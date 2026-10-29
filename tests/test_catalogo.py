import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import wave

from scripts.catalogo import audio_identity, label_reports, register_recording, resolve_audio_path, same_audio, verify_audio_catalog


class AudioCatalogTests(unittest.TestCase):
    def test_verification_excludes_only_explicit_historical_missing_content(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'audio.wav').write_bytes(b'actual')
            current=dict(audio_file='audio.wav',audio_sha256=hashlib.sha256(b'actual').hexdigest())
            historical=dict(audio_file='audio.wav',audio_sha256=hashlib.sha256(b'anterior').hexdigest(),
                            availability_status='historico_sin_wav_coincidente')
            self.assertEqual(verify_audio_catalog([historical,current],root),[current])
            undeclared=dict(historical);undeclared.pop('availability_status')
            with self.assertRaises(ValueError):
                verify_audio_catalog([undeclared,current],root)

    def test_shared_filename_uses_content_hash_and_rejects_obsolete_alias(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'datos/audio').mkdir(parents=True)
            (root/'datos/referencias').mkdir()
            audio = root/'datos/audio/Con trabadas.wav'
            audio.write_bytes(b'actual')
            rows = [dict(id='antigua', audio_file='datos/audio/Con trabadas.wav',
                         audio_sha256=hashlib.sha256(b'anterior').hexdigest(),
                         legacy_audio_files=['datos/audio/antigua.wav']),
                    dict(id='actual', audio_file='datos/audio/Con trabadas.wav',
                         audio_sha256=hashlib.sha256(b'actual').hexdigest())]
            (root/'datos/referencias/catalogo.json').write_text(json.dumps({'recordings':rows}), encoding='utf-8')
            self.assertEqual(audio_identity(audio, root)['id'], 'actual')
            self.assertEqual(resolve_audio_path(audio, root), audio)
            with self.assertRaises(ValueError):
                resolve_audio_path('antigua.wav', root)

    def test_new_recording_renames_wav_preserving_content_and_legacy_references(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'datos/audio').mkdir(parents=True)
            (root/'datos/referencias').mkdir()
            story = root/'cuento.txt'
            story.write_text('Texto.',encoding='utf-8')
            audio = root/'datos/audio/lectura_20261021_120000_000001.wav'
            with wave.open(str(audio),'wb') as w:
                w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(b'\0\0'*160)
            original = audio.read_bytes()
            identity = register_recording(audio,story,'Lectura normal','normal','lector_01','lluvia',root)
            row = json.loads((root/'datos/referencias/catalogo.json').read_text(encoding='utf-8'))['recordings'][0]
            self.assertIn('21/10/2026',identity['label'])
            self.assertEqual(row['reference_status'],'pendiente_revision_usuario')
            self.assertEqual(row['partition'],'sin_asignar')
            renamed = resolve_audio_path(audio, root)
            self.assertFalse(audio.exists())
            self.assertIn('Lectura normal', renamed.name)
            self.assertIn('21-10-2026', renamed.name)
            self.assertTrue(renamed.name.endswith('21-10-2026 - lector_01.wav'))
            self.assertIn('lector_01', identity['label'])
            self.assertEqual(renamed.read_bytes(),original)
            self.assertTrue(same_audio(audio, renamed, root))
            self.assertFalse(same_audio('otro.wav', renamed, root))
            self.assertFalse((root/'datos/referencias/AUDIOS.md').exists())
            self.assertEqual(row['audio_sha256'],hashlib.sha256(original).hexdigest())
            register_recording(audio,story,'Otro nombre',root=root)
            self.assertEqual(len(json.loads((root/'datos/referencias/catalogo.json').read_text(encoding='utf-8'))['recordings']),1)

    def test_unknown_audio_does_not_inherit_another_recording_label(self):
        with tempfile.TemporaryDirectory() as folder:
            identity = audio_identity('desconocido.wav',Path(folder))
            self.assertIsNone(identity['id'])
            self.assertIn('Sin clasificar',identity['label'])

    def test_report_label_is_idempotent_and_keeps_source_json_intact(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'datos/referencias').mkdir(parents=True)
            (root/'resultados/caso').mkdir(parents=True)
            catalog={'recordings':[{'id':'normal','audio_file':'datos/audio/lectura_20261021_120000_000001.wav','label':'Lectura normal · 21/10/2026'}]}
            (root/'datos/referencias/catalogo.json').write_text(json.dumps(catalog),encoding='utf-8')
            source=root/'resultados/caso/resumen.json'
            source.write_text(json.dumps({'audio_file':'lectura_20261021_120000_000001.wav'}),encoding='utf-8')
            report=source.with_suffix('.md');report.write_text('# Resultado\n',encoding='utf-8')
            original=source.read_bytes()
            self.assertEqual(label_reports(root),1)
            first=report.read_text(encoding='utf-8')
            self.assertIn('Lectura normal',first)
            self.assertEqual(label_reports(root),0)
            self.assertEqual(first,report.read_text(encoding='utf-8'))
            self.assertEqual(original,source.read_bytes())
