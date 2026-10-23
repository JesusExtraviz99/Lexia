import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.recursos import compute_summary, compute_markdown, write_resource_report


class ResourceReportTests(unittest.TestCase):
    def test_old_cpu_record_does_not_invent_gpu_telemetry(self):
        result = compute_summary({'device': 'cpu', 'compute_type': 'int8'})
        self.assertFalse(result['gpu_used_for_asr'])
        self.assertEqual(result['resources_status'], 'no_medido_en_la_ejecucion_original')
        self.assertIsNone(result['asr_cpu_seconds'])
        self.assertNotIn('resources', result)

    def test_gpu_global_statistics_do_not_turn_cpu_inference_into_cuda(self):
        resources = {'samples': [], 'gpu_samples': [
            {'gpus': [{'name': 'prueba', 'utilization_percent': 20, 'vram_used_mib': 100,
                       'power_watts': None, 'temperature_celsius': 40}]},
            {'gpus': [{'name': 'prueba', 'utilization_percent': 40, 'vram_used_mib': 200,
                       'power_watts': None, 'temperature_celsius': 42}]}]}
        result = compute_summary({'device': 'cpu', 'resources': resources})
        self.assertFalse(result['gpu_used_for_asr'])
        stats = result['gpu_global_sampled_statistics'][0]
        self.assertEqual(stats['utilization_percent']['mean'], 30)
        self.assertEqual(stats['vram_used_mib']['maximum'], 200)
        self.assertIsNone(stats['power_watts'])

    def test_backfill_preserves_original_json_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root/'run.json'
            source.write_text(json.dumps({'device': 'cpu', 'compute_type': 'int8'}),encoding='utf-8')
            manifest = root/'resumen.json'
            manifest.write_text(json.dumps({'runs': [{'record_file': source.name}]}),encoding='utf-8')
            (root/'resumen.md').write_text('# Resultado original\n',encoding='utf-8')
            hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in [source, manifest]]
            self.assertEqual(write_resource_report(root, root), 1)
            once = (root/'resumen.md').read_text(encoding='utf-8')
            write_resource_report(root, root)
            self.assertEqual(once, (root/'resumen.md').read_text(encoding='utf-8'))
            self.assertEqual(hashes, [hashlib.sha256(p.read_bytes()).hexdigest() for p in [source, manifest]])

    def test_reprocessing_rtf_counts_silence_and_does_not_become_latency(self):
        result = compute_summary({'device': 'cpu', 'audio_seconds': 10, 'block_seconds': 2,
             'updates': [{'processing_seconds': t, 'hypothesis': [], 'asr_cpu_seconds': t*2}
                         for t in [1, 3]]})
        self.assertEqual(result['real_time_factor_full_audio'], .4)
        self.assertEqual(result['asr_cpu_seconds'], 8)
        self.assertEqual(result['over_block_updates'], 1)
        self.assertIsNone(result['real_time_factor_nonempty_hypotheses'])
        self.assertIn('no es latencia visual', compute_markdown([('prueba', {'device':'cpu'})]))
