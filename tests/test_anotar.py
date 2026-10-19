from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from scripts.anotar import Workspace, validate_annotation


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.template = {"duration_seconds": 10, "words": [
            {"index":1,"word":"Ana","start":None,"end":None,"reviewed":False,"note":"","timing_origin":"sin_marcar"},
            {"index":2,"word":"salió","start":None,"end":None,"reviewed":False,"note":"","timing_origin":"sin_marcar"}]}

    def test_asr_times_do_not_become_reviewed(self):
        payload=deepcopy(self.template)
        for w,a,b in zip(payload["words"],(1,2),(2,3)):
            w.update(start=a,end=b,timing_origin="borrador_asr")
        result=validate_annotation(payload,self.template)
        self.assertEqual(result["reviewed_words"],0)
        self.assertEqual(result["timing_status"],"borrador_parcial")

    def test_reject_overlap_and_invalid_times(self):
        for a,b in [(float('nan'),2),(1,11),(3,2)]:
            payload=deepcopy(self.template);payload["words"][0].update(start=a,end=b)
            with self.assertRaises(ValueError):validate_annotation(payload,self.template)
        payload=deepcopy(self.template)
        payload["words"][0].update(start=1,end=3)
        payload["words"][1].update(start=2,end=4)
        with self.assertRaises(ValueError):validate_annotation(payload,self.template)

    def test_require_times_and_preserve_words(self):
        payload=deepcopy(self.template);payload["words"][0]["reviewed"]=True
        with self.assertRaises(ValueError):validate_annotation(payload,self.template)
        payload=deepcopy(self.template);payload["words"][0]["word"]="otra"
        with self.assertRaises(ValueError):validate_annotation(payload,self.template)

    def test_save_creates_backup_in_separate_folder(self):
        workspace=Workspace.__new__(Workspace)
        workspace.template=self.template
        import threading
        workspace.lock=threading.Lock()
        with tempfile.TemporaryDirectory() as folder:
            workspace.path=Path(folder)/'anotacion.json'
            payload=deepcopy(self.template)
            workspace.save(payload)
            payload["words"][0].update(start=1,end=2,reviewed=True,timing_origin="manual")
            result=workspace.save(payload)
            self.assertEqual(result["reviewed_words"],1)
            self.assertEqual(len(list((Path(folder)/'copias').glob('*.json'))),1)
            self.assertFalse(workspace.path.with_suffix('.tmp').exists())


if __name__ == '__main__':unittest.main()
