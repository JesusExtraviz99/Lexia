from contextlib import nullcontext
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np

from scripts import ampliacion_motores as m
from scripts import lanzar_asr_paralelo as launcher


class Tensor:
    def __init__(self, value):self.data=np.array(value)
    @property
    def shape(self):return self.data.shape
    def cpu(self):return self
    def tolist(self):return self.data.tolist()
    def __getitem__(self,index):return Tensor(self.data[index])


class AdapterTests(unittest.TestCase):
    def test_coordinator_accepts_new_manifest_before_starting_worker(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            executable=root/'.venvs/servidor-ampliacion/bin/python'
            executable.parent.mkdir(parents=True);executable.touch()
            folder=root/'modelos/ampliacion/probe'
            folder.mkdir(parents=True)
            (folder/'lexia_modelo_ampliacion.json').write_text('{}')
            specs={'probe':dict(profile='ampliacion',folder='ampliacion/probe',manifest='lexia_modelo_ampliacion.json')}
            commands=[]
            class Process:
                pid=123
                def __init__(self,command,**kwargs):
                    commands.append(command)
                    output=Path(command[command.index('--salida')+1]);output.mkdir()
                    (output/'ejecucion.json').write_text(json.dumps({'selection':{'items':[{'id':'1','sha256':'same','reference':'hola'}]}}))
                    (output/'resumen.json').write_text('{"completed":1,"failures":0}')
                def poll(self):return 0
            argv=['launcher','--dataset','unused','--gpus','0','--salida',str(root/'cohort')]
            with patch.object(launcher,'ROOT',root),patch.object(launcher,'motors',types.SimpleNamespace(SPECS=specs)), \
                    patch.object(launcher.sys,'argv',argv),patch.object(launcher.sys,'platform','linux'), \
                    patch.object(launcher,'is_free',return_value=True),patch.object(launcher,'environment',return_value={}), \
                    patch.object(launcher.subprocess,'Popen',Process),patch.object(launcher.time,'sleep'):
                launcher.main()
            self.assertEqual(len(commands),1)
            self.assertEqual(json.loads((root/'cohort/cohorte.json').read_text())['status'],'completed')

    def fake(self):
        calls=[]
        class Inputs(dict):
            def to(self,device):return self
        class Processor:
            def apply_transcription_request(self, audio, **kwargs):
                calls.append(kwargs)
                return Inputs(input_ids=Tensor([[1,2,3]]))
            def decode(self, value, **kwargs):
                calls.append(('decode',value.tolist(),kwargs))
                return 'hola'
            def batch_decode(self,value,**kwargs):return ['hola']
        class Model:
            def eval(self):return self
            def to(self,device):return self
            def parameters(self):return []
            def generate(self,**kwargs):return Tensor([[1,2,3,4,5]])
        factory=types.SimpleNamespace(from_pretrained=lambda *a,**kw:(Model(),{}))
        tf=types.SimpleNamespace(AutoProcessor=types.SimpleNamespace(from_pretrained=lambda *a,**kw:Processor()),
            AutoModelForSpeechSeq2Seq=factory,AutoModelForCTC=factory,Qwen3ASRForConditionalGeneration=factory)
        torch=types.SimpleNamespace(set_num_threads=lambda n:None,manual_seed=lambda n:None,
            backends=types.SimpleNamespace(cudnn=types.SimpleNamespace(benchmark=True)),float32='float32',inference_mode=nullcontext)
        return calls,{'torch':torch,'transformers':tf}

    def test_qwen_strips_input_prompt_before_decoding(self):
        calls,modules=self.fake()
        with patch.dict('sys.modules',modules):
            infer,_=m.load('qwen_asr_06b','unused',None,4)
            result=infer(np.zeros(16000))
        self.assertEqual(result['token_ids'],[4,5])
        self.assertEqual(calls[0]['language'],'Spanish')
        self.assertEqual(calls[1][2]['return_format'],'transcription_only')

    def test_canary_transcribes_spanish_without_translation(self):
        calls,modules=self.fake()
        with patch.dict('sys.modules',modules):
            infer,_=m.load('canary_v2','unused',None,4)
            result=infer(np.zeros(16000))
        self.assertEqual(calls[0]['source_language'],'es')
        self.assertEqual(calls[0]['target_language'],'es')
        self.assertEqual(result['hypothesis'],'hola')

    def test_literal_models_excluded_from_test_registry(self):
        self.assertEqual(len(m.KEYS),7)
        self.assertFalse(any(key.startswith('crisper') for key in m.KEYS))
        with self.assertRaises(ValueError):m.check('unused','crisper_medium',lambda p:'unused')


if __name__=='__main__':unittest.main()
