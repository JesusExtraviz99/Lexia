from dataclasses import dataclass
from contextlib import nullcontext
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

import numpy as np

from scripts import asr_motores_externos as m
from scripts import evaluar_asr_externo as e
from scripts import lanzar_asr_paralelo as launcher


class AdapterTests(unittest.TestCase):
    def test_test_partition_needs_confirmation_and_plan_has_no_side_effects(self):
        argv = ['launcher', '--dataset', 'unused', '--gpus', '0', '1', '2', '3',
                '--particion', 'test', '--limite', '0', '--completo', '--salida', 'unused', '--plan']
        with patch.object(launcher.sys, 'argv', argv), patch('sys.stderr', new_callable=io.StringIO):
            with self.assertRaises(SystemExit) as error:
                launcher.main()
            self.assertEqual(error.exception.code, 2)
        with patch.object(launcher.sys, 'argv', argv+['--confirmar-test']), \
                patch('sys.stdout', new_callable=io.StringIO) as output, \
                patch.object(launcher.subprocess, 'Popen') as process:
            launcher.main()
            process.assert_not_called()
            plan = json.loads(output.getvalue())
            self.assertEqual(plan['partition'], 'test')
            self.assertTrue(plan['full_partition'])
            self.assertFalse(plan['full_dev'])

    def test_sequential_four_motors_never_overlap_and_exclude_crisper(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            motors = ['xlsr', 'parakeet', 'whisper', 'vosk']
            for motor in motors:
                spec = m.SPECS[motor]
                executable = root/'.venvs'/('servidor-'+spec['profile'])/'bin/python'
                executable.parent.mkdir(parents=True, exist_ok=True)
                executable.touch()
                model = root/'modelos'/spec['folder']/'lexia_modelo.json'
                model.parent.mkdir(parents=True)
                model.write_text('{}')
            commands, active = [], []
            class Process:
                def __init__(self, command, **kwargs):
                    if active:
                        raise AssertionError('Motores solapados')
                    active.append(self)
                    commands.append(command)
                    self.pid = 100+len(commands)
                    self.returncode = 0
                    output = Path(command[command.index('--salida')+1])
                    output.mkdir()
                    (output/'ejecucion.json').write_text(json.dumps({'selection': {'items': [
                        {'id': '1_2_3', 'sha256': 'same', 'reference': 'hola'}]}}))
                    (output/'resumen.json').write_text('{"completed":100,"failures":0}')
                def poll(self):
                    active.remove(self)
                    return 0
            argv = ['launcher', '--dataset', str(root/'data'), '--gpus', '0', '--secuencial',
                    '--motores', *motors, '--limite', '100', '--salida', str(root/'cohort')]
            with patch.object(launcher, 'ROOT', root), patch.object(launcher.sys, 'argv', argv), \
                    patch.object(launcher.sys, 'platform', 'linux'), \
                    patch.object(launcher, 'is_free', return_value=True) as free, \
                    patch.object(launcher, 'environment', return_value={}), \
                    patch.object(launcher.subprocess, 'Popen', Process), \
                    patch.object(launcher.time, 'sleep'):
                launcher.main()
            self.assertEqual([c[c.index('--motor')+1] for c in commands], motors)
            self.assertTrue(all(c[c.index('--modo-ejecucion')+1] == 'aislada' for c in commands))
            self.assertTrue(all(call.args == (0,) for call in free.call_args_list))
            self.assertNotIn('--gpu', commands[-1])
            self.assertTrue(all(c[c.index('--gpu')+1] == '0' for c in commands[:-1]))
            self.assertEqual(json.loads((root/'cohort/cohorte.json').read_text())['status'], 'completed')

    def test_sequential_rejects_multiple_gpu(self):
        argv = ['launcher', '--dataset', 'unused', '--gpus', '0', '1', '--secuencial',
                '--salida', 'unused', '--plan']
        with patch.object(launcher.sys, 'argv', argv), patch('sys.stderr', new_callable=io.StringIO):
            with self.assertRaises(SystemExit) as error:
                launcher.main()
            self.assertEqual(error.exception.code, 2)

    def test_full_dev_requires_explicit_flag_and_plan_does_not_launch(self):
        base = ['launcher', '--dataset', 'unused', '--gpus', '0', '1', '2', '3',
                '--limite', '0', '--salida', 'unused', '--plan']
        with patch.object(launcher.sys, 'argv', base), patch('sys.stderr', new_callable=io.StringIO):
            with self.assertRaises(SystemExit) as error:
                launcher.main()
            self.assertEqual(error.exception.code, 2)
        with patch.object(launcher.sys, 'argv', base+['--completo']), \
                patch('sys.stdout', new_callable=io.StringIO) as output, \
                patch.object(launcher.subprocess, 'Popen') as process:
            launcher.main()
            process.assert_not_called()
            self.assertTrue(json.loads(output.getvalue())['full_dev'])

    def torch_stub(self):
        return types.SimpleNamespace(set_num_threads=lambda n: None, manual_seed=lambda n: None,
            backends=types.SimpleNamespace(cudnn=types.SimpleNamespace(benchmark=True)),
            cuda=types.SimpleNamespace(is_available=lambda: True, device_count=lambda: 1,
                                       synchronize=lambda: None),
            inference_mode=nullcontext, float32='float32')

    def test_parakeet_decodes_sequences_not_modeloutput(self):
        calls = []
        class Sequences:
            shape = (1, 2)
            def cpu(self): return self
            def tolist(self): return [[1, 2]]
        sequences = Sequences()
        class Inputs(dict):
            def to(self, device):
                calls.append(device)
                return self
        class Processor:
            def __call__(self, *args, **kwargs): return Inputs(signal='fake')
            def batch_decode(self, value, **kwargs):
                if value is not sequences: raise AssertionError('Wrong decode input')
                return ['hola']
        class Model:
            def eval(self): return self
            def to(self, device): return self
            def parameters(self): return []
            def generate(self, **kwargs):
                calls.append(kwargs)
                return types.SimpleNamespace(sequences=sequences)
        fake = types.SimpleNamespace(
            AutoProcessor=types.SimpleNamespace(from_pretrained=lambda *a, **k: Processor()),
            AutoModelForTDT=types.SimpleNamespace(from_pretrained=lambda *a, **k: Model()))
        with patch.dict('sys.modules', {'torch': self.torch_stub(), 'transformers': fake}):
            infer, _ = m.load('parakeet', 'unused', 1, 4)
            result = infer(np.zeros(10, dtype=np.float32))
        self.assertEqual(result['hypothesis'], 'hola')
        self.assertEqual(result['token_ids'], [1, 2])
        self.assertFalse(result['generation_cap_reached'])
        self.assertEqual(calls[0], 'cuda:0')
        self.assertEqual(calls[1]['max_new_tokens'], 512)

    def test_crisper_preserves_verbatim_options_and_native_output(self):
        calls = []
        @dataclass
        class Result:
            text: str
        class Crisper:
            def __init__(self, *a, **kwargs): calls.append(kwargs)
            def transcribe(self, signal, **kwargs):
                calls.append(kwargs)
                return Result('re- regresaron')
        with patch.dict('sys.modules', {'torch': self.torch_stub(),
                'crisperwhisper': types.SimpleNamespace(CrisperWhisperModel=Crisper)}):
            infer, _ = m.load('crisper', 'unused', 3, 4)
            result = infer(np.zeros(10, dtype=np.float32))
        self.assertEqual(calls[0]['backend'], 'transformers')
        self.assertEqual(calls[0]['device'], 'cuda')
        self.assertEqual(calls[1]['mode'], 'verbatim')
        self.assertEqual(calls[1]['language'], 'es')
        self.assertEqual(result['native_result']['text'], 're- regresaron')
        self.assertIsNone(result['forward_seconds'])

    def test_zip_path_rejects_escape_and_unexpected_root(self):
        root = Path.cwd()
        for name in ['../outside', '/outside', 'other/file', 'model/../../x', 'model/C:x', 'model\\x']:
            with self.assertRaises(ValueError):
                m.safe_member(name, root, 'model')
        self.assertEqual(m.safe_member('model/a/b', root, 'model'), root/'model/a/b')

    def test_whisper_consumes_lazy_segments_and_passes_no_external_vad(self):
        calls = []
        @dataclass
        class Segment:
            text: str
            tokens: list
        class Whisper:
            def __init__(self, *args, **kwargs):
                self.kwargs = kwargs
            def transcribe(self, signal, **kwargs):
                calls.append(kwargs)
                def segments():
                    calls.append('generator consumed')
                    yield Segment(' hola', [1])
                    yield Segment(' mundo', [2])
                return segments(), types.SimpleNamespace(language_probability=.9)
        with patch.dict('sys.modules', {'faster_whisper': types.SimpleNamespace(WhisperModel=Whisper)}):
            infer, torch = m.load('whisper', 'unused', 2, 4)
            result = infer(np.zeros(10, dtype=np.float32))
        self.assertIsNone(torch)
        self.assertEqual(result['hypothesis'], 'hola mundo')
        self.assertIn('generator consumed', calls)
        self.assertFalse(calls[0]['vad_filter'])
        self.assertFalse(calls[0]['condition_on_previous_text'])
        self.assertIsNone(result['forward_seconds'])

    def test_vosk_keeps_intermediate_results_and_final_and_clips_pcm(self):
        chunks = []
        class Recognizer:
            def __init__(self, model, sr):
                pass
            def SetWords(self, value):
                pass
            def AcceptWaveform(self, value):
                chunks.append(value)
                return True
            def Result(self):
                return '{"text":"hola"}'
            def FinalResult(self):
                return '{"text":"mundo"}'
        fake = types.SimpleNamespace(Model=lambda p: object(), KaldiRecognizer=Recognizer)
        with patch.dict('sys.modules', {'vosk': fake}):
            infer, torch = m.load('vosk', 'unused', None, 4)
            result = infer(np.array([-2, -1, 0, 1, 2], dtype=np.float32))
            with self.assertRaisesRegex(ValueError, 'CPU'):
                m.load('vosk', 'unused', 0, 4)
        self.assertEqual(result['hypothesis'], 'hola mundo')
        self.assertEqual(np.frombuffer(chunks[0], dtype='<i2').tolist(), [-32768, -32768, 0, 32767, 32767])
        self.assertIsNone(torch)

    def test_gpu_telemetry_keeps_own_memory_and_counts_others(self):
        first = types.SimpleNamespace(returncode=0, stdout='100, 20, 10, 40, 55, 1500, 7000\n')
        second = types.SimpleNamespace(returncode=0, stdout=f'{e.os.getpid()}, 80\n987654, 12\n')
        with patch.object(e.subprocess, 'run', side_effect=[first, second]):
            result = e.gpu_sample(2)
        self.assertEqual(result['process_vram_mib'], 80)
        self.assertEqual(result['other_compute_process_count'], 1)
        self.assertNotIn('987654', json.dumps(result))

    def test_coordinator_uses_only_explicit_gpus_and_cpu_for_vosk(self):
        self.run_coordinator_case('dev')

    def test_coordinator_propagates_test_confirmation_to_every_motor(self):
        self.run_coordinator_case('test')

    def run_coordinator_case(self, partition):
        commands = []
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for profile in ['transformers', 'whisper', 'crisper', 'vosk']:
                path = root/'.venvs'/('servidor-'+profile)/'bin/python'
                path.parent.mkdir(parents=True)
                path.touch()
            for spec in m.SPECS.values():
                path = root/'modelos'/spec['folder']/'lexia_modelo.json'
                path.parent.mkdir(parents=True)
                path.write_text('{}')
            class Process:
                returncode = 0
                def __init__(self, command, **kwargs):
                    self.pid = 100+len(commands)
                    commands.append(command)
                    out = Path(command[command.index('--salida')+1])
                    out.mkdir(parents=True)
                    (out/'ejecucion.json').write_text(json.dumps({'selection':{'items':[
                        {'id':'1_2_3', 'sha256':'same', 'reference':'hola'}]}}))
                    (out/'resumen.json').write_text('{"completed":1,"failures":0}')
                def poll(self):
                    return 0
            argv = ['launcher', '--dataset', str(root/'data'), '--gpus', '2', '--salida', str(root/'cohort')]
            if partition == 'test':
                argv += ['--particion', 'test', '--confirmar-test', '--limite', '0', '--completo']
            with patch.object(launcher, 'ROOT', root), patch.object(launcher.sys, 'argv', argv), \
                    patch.object(launcher.sys, 'platform', 'linux'), \
                    patch.object(launcher, 'is_free', return_value=True), \
                    patch.object(launcher, 'environment', return_value={}), \
                    patch.object(launcher.subprocess, 'Popen', Process), \
                    patch.object(launcher.time, 'sleep'):
                launcher.main()
            state = json.loads((root/'cohort/cohorte.json').read_text())
            self.assertEqual(state['status'], 'completed')
            self.assertEqual(state['partition'], partition)
            self.assertEqual(len(commands), 5)
            for command in commands:
                motor = command[command.index('--motor')+1]
                self.assertEqual(command[command.index('--particion')+1], partition)
                self.assertEqual('--confirmar-test' in command, partition == 'test')
                if motor == 'vosk':
                    self.assertNotIn('--gpu', command)
                else:
                    self.assertEqual(command[command.index('--gpu')+1], '2')
            self.assertTrue(state['selection_equal'])


if __name__ == '__main__':
    unittest.main()
