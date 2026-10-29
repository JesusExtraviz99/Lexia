import tarfile
import unittest
from pathlib import Path
from scripts.importar_fleurs import member_target


class SafeFleursExtractionTests(unittest.TestCase):
    def test_regular_audio_stays_inside_split(self):
        root=Path.cwd()/'datos/externos/fleurs_es_419/prueba_no_creada'
        member=tarfile.TarInfo('dev/example.wav');member.size=100
        self.assertEqual(member_target(member,'dev',root),root.resolve()/'dev/example.wav')

    def test_traversal_absolute_drive_and_wrong_split_are_rejected(self):
        root=Path.cwd()/'datos/externos/fleurs_es_419/prueba_no_creada'
        for name in ['../escape.wav','/dev/escape.wav','C:/escape.wav','dev/../../escape.wav','dev\\escape.wav','test/escape.wav']:
            with self.subTest(name=name),self.assertRaises(ValueError):
                member_target(tarfile.TarInfo(name),'dev',root)

    def test_links_are_not_extracted(self):
        for kind in [tarfile.SYMTYPE,tarfile.LNKTYPE]:
            member=tarfile.TarInfo('dev/link.wav');member.type=kind
            with self.assertRaises(ValueError):
                member_target(member,'dev',Path.cwd())


if __name__=='__main__':unittest.main()
