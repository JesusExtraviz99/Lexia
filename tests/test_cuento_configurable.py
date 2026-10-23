from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import comparar_ventanas, grabar


class ConfigurableStoryTests(unittest.TestCase):
    def test_comparison_forwards_selected_story_and_records_its_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            story = root / 'otro cuento.txt'
            story.write_text('Luna vio estrellas.', encoding='utf-8')
            audio = root / 'lectura.wav'
            def child(command, **kwargs):
                selected = Path(command[command.index('--cuento')+1])
                self.assertEqual(selected, story.resolve())
                output = Path(command[command.index('--salida')+1])
                output.write_text(json.dumps({'story_words': ['Luna', 'vio', 'estrellas'],
                    'block_seconds': 2, 'updates': [{'processing_seconds': 1,
                    'audio_available_seconds': 2, 'audio_reprocessed_seconds': 2,
                    'backlog_seconds_simulated': 0, 'sequential_ready_seconds_simulated': 3,
                    'position': 3, 'movement': 3}]}), encoding='utf-8')
            argv = ['comparar_ventanas', str(audio), '--cuento', str(story), '--ventanas', '4', '8']
            with patch.object(comparar_ventanas, 'ROOT', root), patch('sys.argv', argv), \
                    patch.object(comparar_ventanas.subprocess, 'run', side_effect=child) as run, \
                    redirect_stdout(io.StringIO()):
                comparar_ventanas.main()
            self.assertEqual(run.call_count, 2)
            manifest = next((root/'resultados/comparaciones').glob('*/resumen.json'))
            data = json.loads(manifest.read_text(encoding='utf-8'))
            self.assertEqual(data['story_file'], str(story.resolve()))
            self.assertEqual(data['story_sha256'], hashlib.sha256(story.read_bytes()).hexdigest())
            self.assertEqual([r['final_position'] for r in data['runs']], [3, 3])

    def test_recording_shows_selected_story_and_still_waits_for_enter(self):
        class StopBeforeRecording(Exception):
            pass
        with tempfile.TemporaryDirectory() as tmp:
            story = Path(tmp)/'otro cuento.txt'
            story.write_text('Luna vio estrellas.', encoding='utf-8')
            output = io.StringIO()
            with patch('sys.argv', ['grabar', '--cuento', str(story)]), \
                    patch.object(grabar.sd, 'query_devices', return_value={'name': 'prueba', 'default_samplerate': 16000}), \
                    patch.object(grabar.sd, 'rec') as record, \
                    patch('builtins.input', side_effect=StopBeforeRecording), redirect_stdout(output):
                with self.assertRaises(StopBeforeRecording):
                    grabar.main()
            record.assert_not_called()
            self.assertIn('Luna vio estrellas.', output.getvalue())
