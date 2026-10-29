"""Captura simulada: ninguna prueba consulta o activa un micrófono."""
import unittest
from unittest.mock import patch
import numpy as np
from scripts import grabar


class SimulatedStream:
    def __init__(self, data, **kwargs):
        self.data = data
        self.callback = kwargs['callback']
        self.finished = kwargs['finished_callback']

    def __enter__(self):
        if len(self.data):
            try:
                self.callback(self.data, len(self.data), None, None)
            except grabar.sd.CallbackStop:
                self.finished()
        return self

    def __exit__(self, *args):
        self.finished()


class ManualRecordingTests(unittest.TestCase):
    def test_long_reading_allows_eight_minutes_but_waits_for_start(self):
        args = ['grabar', '--segundos', '480', '--parar-con-enter',
                '--cuento', str(grabar.ROOT/'datos/textos/lectura_05.txt')]
        with patch('sys.argv', args), \
             patch.object(grabar.sd, 'query_devices', return_value={'name': 'simulado', 'default_samplerate': 16000}), \
             patch('builtins.input', side_effect=EOFError), patch('builtins.print'), \
             patch.object(grabar.sd, 'InputStream') as stream:
            with self.assertRaises(EOFError):
                grabar.main()
            stream.assert_not_called()

    def capture(self, values):
        data = np.array(values, dtype=np.float32).reshape(-1, 1)
        with patch.object(grabar.sd, 'InputStream', side_effect=lambda **kw: SimulatedStream(data, **kw)):
            return grabar.record_until_enter(1, 5, None, stop_requested=lambda: True)

    def test_manual_stop_keeps_only_received_samples_without_padding(self):
        np.testing.assert_array_equal(self.capture([.1, .2, .3]),
                                      np.array([[.1], [.2], [.3]], dtype=np.float32))

    def test_automatic_limit_truncates_last_callback_exactly(self):
        np.testing.assert_array_equal(self.capture([1, 2, 3, 4, 5, 6, 7]),
                                      np.array([[1], [2], [3], [4], [5]], dtype=np.float32))

    def test_empty_capture_is_not_saved(self):
        with self.assertRaisesRegex(ValueError, 'No se han recibido muestras'):
            self.capture([])


if __name__ == '__main__':
    unittest.main()
