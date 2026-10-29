import unittest
from unittest.mock import patch

from scripts.grabar_lector import build_command, required, main


class SingleRecordingTests(unittest.TestCase):
    def test_selected_story_reader_and_manual_stop_are_forwarded(self):
        command = build_command('lectura_03.txt', 'Lectura normal', 'normal', 'lector_02', 'aula', 4)
        self.assertEqual(command[command.index('--cuento') + 1], 'lectura_03.txt')
        self.assertEqual(command[command.index('--lector') + 1], 'lector_02')
        self.assertIn('--parar-con-enter', command)
        self.assertEqual(command[command.index('--dispositivo') + 1], '4')

    @patch('builtins.input', side_effect=['../lector', '', 'lector_03'])
    def test_reader_id_cannot_be_a_path(self, _):
        self.assertEqual(required('ID: ', reader=True), 'lector_03')

    @patch('scripts.grabar_lector.subprocess.run')
    @patch('builtins.input', side_effect=['2', 'lector_02', '1', ''])
    @patch('sys.argv', ['grabar_lector'])
    def test_menu_starts_exactly_one_recording(self, _, run):
        run.return_value.returncode = 0
        main()
        self.assertEqual(run.call_count, 1)
        command = run.call_args.args[0]
        self.assertTrue(command[command.index('--cuento') + 1].endswith('lectura_02.txt'))

