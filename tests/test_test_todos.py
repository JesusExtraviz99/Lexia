import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
from scripts import lanzar_test_todos as t
from scripts import lanzar_asr_paralelo as launcher


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data),encoding='utf-8')


class CombinedTests(unittest.TestCase):
    def test_pid_probe_never_signals_processes_on_windows(self):
        with patch.object(t.os,'name','nt'),patch.object(t.os,'kill') as kill:
            self.assertFalse(t.is_alive(123))
            kill.assert_not_called()
    def fixture(self,root):
        legacy=root/'legacy';base=legacy/'vosk'
        items=[dict(id='1_2_3',sha256='same',reference='hola')]
        config=dict(model={'revision':'pinned'},parameters={'batch':1},selection={'items':items},gpu_physical_index=None)
        sig=t.e.signature(config)
        save(base/'ejecucion.json',dict(**config,run_signature=sig))
        save(base/'progreso.json',dict(status='completed',pid=123))
        save(base/'resumen.json',dict(completed=1,failures=0))
        save(base/'audios/1_2_3.json',dict(**items[0],status='ok',run_signature=sig))
        protocol={'models':{'vosk':{'model':config['model'],'parameters':config['parameters']}}}
        output=root/'out';output.mkdir()
        return legacy,items,protocol,output

    def test_reuses_only_identical_complete_results_and_keeps_original(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);legacy,items,protocol,output=self.fixture(root)
            result=t.reuse_legacy('vosk',output,legacy,items,protocol)
            self.assertTrue(result['reused'])
            self.assertEqual((output/'vosk/audios/1_2_3.json').read_bytes(),(legacy/'vosk/audios/1_2_3.json').read_bytes())

    def test_rejects_different_configuration(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);legacy,items,protocol,output=self.fixture(root)
            protocol['models']['vosk']['parameters']={'batch':2}
            with self.assertRaises(ValueError):t.reuse_legacy('vosk',output,legacy,items,protocol)
            self.assertFalse((output/'vosk').exists())

    def test_running_previous_worker_is_waited_not_duplicated(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);legacy,items,protocol,output=self.fixture(root)
            save(legacy/'vosk/progreso.json',dict(status='running',pid=999))
            with patch.object(t,'is_alive',return_value=True):
                self.assertEqual(t.reuse_legacy('vosk',output,legacy,items,protocol),'wait')
            self.assertFalse((output/'vosk').exists())

    def test_coordinator_does_not_launch_reused_model(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            exe=root/'.venvs/servidor-vosk/bin/python';exe.parent.mkdir(parents=True);exe.touch()
            model=root/'modelos/vosk/lexia_modelo.json';model.parent.mkdir(parents=True);model.write_text('{}')
            def reuse(motor,folder):
                save(folder/motor/'ejecucion.json',{'selection':{'items':[{'id':'1','sha256':'same','reference':'hola'}]}})
                save(folder/motor/'resumen.json',{'completed':1})
                return dict(motor=motor,status='completed',gpu=None,returncode=0,reused=True)
            argv=['launcher','--dataset','unused','--gpus','0','--salida',str(root/'cohort')]
            with patch.object(launcher,'ROOT',root),patch.object(launcher,'reuse_result',reuse), \
                    patch.object(launcher,'motors',types.SimpleNamespace(SPECS={'vosk':dict(folder='vosk',profile='vosk')})), \
                    patch.object(launcher.sys,'argv',argv),patch.object(launcher.sys,'platform','linux'), \
                    patch.object(launcher,'is_free',return_value=True),patch.object(launcher.subprocess,'Popen') as process:
                launcher.main();process.assert_not_called()
            self.assertEqual(t.read(root/'cohort/cohorte.json')['status'],'completed')


if __name__=='__main__':unittest.main()
