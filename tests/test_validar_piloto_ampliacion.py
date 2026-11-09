import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts import validar_piloto_ampliacion as v


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')


class PilotTests(unittest.TestCase):
    def fixture(self,root):
        jobs=[dict(motor=key,status='completed',returncode=0) for key in v.KEYS]
        save(root/'cohorte.json',dict(status='completed',jobs=jobs))
        items=[dict(id=str(n),sha256='same',reference='hola') for n in range(10)]
        for key in v.KEYS:
            config=dict(selection=dict(split='dev',items=items),
                adapter_sha256=hashlib.sha256((Path(v.__file__).parent/'ampliacion_motores.py').read_bytes()).hexdigest(),
                script_sha256=hashlib.sha256((Path(v.__file__).parent/'evaluar_asr_externo.py').read_bytes()).hexdigest())
            sig=hashlib.sha256(json.dumps(config,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            save(root/key/'ejecucion.json',dict(**config,run_signature=sig))
            save(root/key/'resumen.json',dict(completed=10,failures=0))
            for item in items:
                save(root/key/'audios'/(item['id']+'.json'),dict(**item,status='ok',run_signature=sig,native_output={}))

    def test_accepts_complete_pilot_and_rejects_missing_audio(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root)
            self.assertEqual(v.validate(root)['motors'],7)
            (root/v.KEYS[0]/'audios/0.json').unlink()
            with self.assertRaises(ValueError):v.validate(root)

    def test_generation_limit_stops_full_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root)
            path=root/v.KEYS[0]/'audios/0.json'
            record=v.read(path);record['native_output']['generation_cap_reached']=True;save(path,record)
            with self.assertRaisesRegex(ValueError,'límite de generación'):v.validate(root)

    def test_failed_worker_stops_full_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root)
            path=root/'cohorte.json';c=v.read(path);c['jobs'][0]['returncode']=1;save(path,c)
            with self.assertRaisesRegex(ValueError,'no completado'):v.validate(root)


if __name__=='__main__':unittest.main()
