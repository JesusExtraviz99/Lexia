import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

import numpy as np
import soundfile as sf

from scripts import evaluar_asr_externo as e


@unittest.skipUnless(importlib.util.find_spec('jiwer') and importlib.util.find_spec('psutil'),
                     'Requiere dependencias de validación jiwer/psutil; usar el entorno aislado documentado.')
class ExternalEvaluationTests(unittest.TestCase):
    def make_dataset(self, root):
        folder = root/'dev'
        audio = folder/'audio/1/2'
        audio.mkdir(parents=True)
        lines = []
        for i in range(4):
            key = f'1_2_{i}'
            sf.write(audio/f'{key}.flac', np.zeros(1600, dtype=np.float32), 16000)
            lines.append(key+'\tUna mañana azul')
        (folder/'transcripts.txt').write_text('\n'.join(lines), encoding='utf-8')

    def test_selection_reproducible_and_reference_audio_ids_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_dataset(root)
            first = e.select_mls(root, 'dev', 2, 42)
            self.assertEqual(first, e.select_mls(root, 'dev', 2, 42))
            self.assertEqual(len(first['items']), 2)
            self.assertEqual(len(e.select_mls(root, 'dev', 0, 42)['items']), 4)
            next((root/'dev/audio').rglob('*.flac')).unlink()
            with self.assertRaisesRegex(ValueError, 'no coinciden'):
                e.select_mls(root, 'dev', 2, 42)

    def test_normalization_and_empty_speech_output_are_scored_as_errors(self):
        self.assertEqual(e.normalized('¡Árbol, NIÑA!'), 'árbol niña')
        metrics = e.score('Una mañana azul', 'UNA mañana')
        self.assertEqual(metrics['deletions'], 1)
        self.assertAlmostEqual(metrics['wer'], 1/3)
        empty = e.score('Una mañana azul', '')
        self.assertEqual(empty['wer'], 1)
        self.assertEqual(empty['deletions'], 3)

    def test_energy_does_not_extrapolate_or_treat_unavailable_as_zero(self):
        result = e.resource_summary([], [dict(elapsed_seconds=1, power_watts=20),
            dict(elapsed_seconds=3, power_watts=30), dict(elapsed_seconds=10, power_watts=None)])
        self.assertEqual(result['gpu_energy_sampled_interval_joules'], 50)
        self.assertEqual(result['gpu_energy_coverage_seconds'], 2)
        self.assertIsNone(result['rss_bytes'])
        self.assertIsNone(e.resource_summary([], [])['gpu_energy_sampled_interval_joules'])

    def test_corpus_wer_uses_word_counts_and_failures_are_separate(self):
        records = []
        for ref, hyp in [('uno dos tres', 'uno dos'), ('uno', '')]:
            records.append(dict(status='ok', accuracy=e.score(ref, hyp), audio_seconds=1,
                                timing=dict(asr_seconds=.1, asr_rtf=.1)))
        records.append(dict(status='error', error='simulated'))
        summary = e.aggregate(records)
        self.assertEqual(summary['failures'], 1)
        self.assertEqual(summary['completed'], 2)
        self.assertEqual(summary['corpus_wer'], .5)
        self.assertNotEqual(summary['corpus_wer'], summary['per_audio_wer']['mean'])

    def fake_model(self):
        return dict(**e.SPEC, files=[dict(file='mock', bytes=1, sha256='fake')])

    def args(self, root):
        return argparse.Namespace(dataset=root/'data', modelo=root/'model', salida=root/'out',
            particion='dev', confirmar_test=False, limite=2, semilla=42, hilos=4, gpu=None,
            reanudar=False)

    def fake_loader(self, *_):
        def infer(signal):
            return dict(hypothesis='Una mañana azul', prepare_seconds=0, forward_seconds=0,
                        decode_seconds=0, token_ids=[1, 2])
        return infer, types.SimpleNamespace(version=types.SimpleNamespace(cuda=None))

    def test_pipeline_reports_resume_and_rejects_config_drift_without_real_asr(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_dataset(root/'data')
            args = self.args(root)
            with patch.object(e, 'check_model', return_value=self.fake_model()), \
                    patch.object(e.importlib.metadata, 'version', return_value='test-stub'), \
                    patch.object(e, 'load_xlsr', side_effect=self.fake_loader) as loader:
                e.run(args)
                summary = json.loads((root/'out/resumen.json').read_text(encoding='utf-8'))
                self.assertEqual(summary['completed'], 2)
                self.assertEqual(summary['corpus_wer'], 0)
                incremental = list((root/'out/sesiones').glob('*.jsonl'))
                self.assertEqual(len(incremental), 1)
                self.assertEqual(json.loads(incremental[0].read_text(encoding='utf-8').splitlines()[0])['kind'], 'start')
                loader.assert_called_once()
                args.reanudar = True
                e.run(args)
                loader.assert_called_once()
                args.semilla = 43
                with self.assertRaisesRegex(ValueError, 'exactamente'):
                    e.run(args)

    def test_failure_persisted_before_stopping_and_no_automatic_retry(self):
        calls = []
        def loader(*_):
            def infer(signal):
                calls.append(1)
                if len(calls) > 1:
                    raise RuntimeError('simulated failure')
                return dict(hypothesis='', prepare_seconds=0, forward_seconds=0,
                            decode_seconds=0, token_ids=[])
            return infer, types.SimpleNamespace(version=types.SimpleNamespace(cuda=None))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_dataset(root/'data')
            args = self.args(root)
            args.limite = 1
            with patch.object(e, 'check_model', return_value=self.fake_model()), \
                    patch.object(e.importlib.metadata, 'version', return_value='test-stub'), \
                    patch.object(e, 'load_xlsr', side_effect=loader):
                with self.assertRaisesRegex(RuntimeError, 'simulated failure'):
                    e.run(args)
                summary = json.loads((root/'out/resumen.json').read_text(encoding='utf-8'))
                self.assertEqual(summary['failures'], 1)
                self.assertIsNone(summary['corpus_wer'])
                args.reanudar = True
                with self.assertRaisesRegex(RuntimeError, 'fallos guardados'):
                    e.run(args)
                self.assertEqual(len(calls), 2)

    def test_full_dev_keeps_all_results_with_periodic_reports(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_dataset(root/'data')
            args = self.args(root)
            args.limite = 0
            args.informar_cada = 2
            original = e.write_reports
            with patch.object(e, 'check_model', return_value=self.fake_model()), \
                    patch.object(e.importlib.metadata, 'version', return_value='test-stub'), \
                    patch.object(e, 'load_xlsr', side_effect=self.fake_loader), \
                    patch.object(e, 'write_reports', wraps=original) as reports:
                e.run(args)
            self.assertEqual(reports.call_count, 3)  # cortes 2/4 y cierre
            self.assertEqual(len(list((root/'out/audios').glob('*.json'))), 4)
            progress = json.loads((root/'out/progreso.json').read_text(encoding='utf-8'))
            self.assertEqual((progress['status'], progress['completed'], progress['selected']), ('completed', 4, 4))
            summary = json.loads((root/'out/resumen.json').read_text(encoding='utf-8'))
            self.assertEqual(summary['corpus_wer'], 0)

    def test_interrupted_audio_can_resume_and_previous_attempt_is_preserved(self):
        calls = []
        def loader(*_):
            def infer(signal):
                calls.append(1)
                if len(calls) == 2:
                    raise KeyboardInterrupt()
                return dict(hypothesis='Una mañana azul', prepare_seconds=0, forward_seconds=0,
                            decode_seconds=0, token_ids=[1])
            return infer, types.SimpleNamespace(version=types.SimpleNamespace(cuda=None))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_dataset(root/'data')
            args = self.args(root)
            args.limite = 1
            with patch.object(e, 'check_model', return_value=self.fake_model()), \
                    patch.object(e.importlib.metadata, 'version', return_value='test-stub'), \
                    patch.object(e, 'load_xlsr', side_effect=loader):
                with self.assertRaises(KeyboardInterrupt):
                    e.run(args)
                partial = json.loads(next((root/'out/audios').glob('*.json')).read_text(encoding='utf-8'))
                self.assertEqual(partial['status'], 'interrupted')
                args.reanudar = True
                e.run(args)
            prior = list((root/'out/intentos').glob('*.json'))
            self.assertEqual(len(prior), 1)
            self.assertEqual(json.loads(prior[0].read_text(encoding='utf-8'))['status'], 'interrupted')
            summary = json.loads((root/'out/resumen.json').read_text(encoding='utf-8'))
            self.assertEqual((summary['completed'], summary['failures']), (1, 0))


if __name__ == '__main__':
    unittest.main()
