import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from scripts.directo_local import LocalEngine,pcm_window


class LiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);(self.root/'datos/textos').mkdir(parents=True)
        (self.root/'datos/textos/lectura_01.txt').write_text('Una mañana Ana salió de casa.',encoding='utf-8')
        self.engine=LocalEngine(self.root,infer=lambda x:dict(hypothesis='Una mañana Ana'))
        self.pcm=np.ones(32000,dtype='<f4').tobytes()

    def test_positions_persist_without_audio_and_finish_rejects_more(self):
        session=self.engine.start('lectura_01.txt');ident=session['id']
        r=self.engine.update(ident,self.pcm,16000,2)
        self.assertEqual(r['position'],3)
        r=self.engine.update(ident,self.pcm,16000,4)
        self.assertEqual(r['mode'],'hipotesis_sin_cambios')
        self.engine.event(dict(id=ident,kind='finish'))
        with self.assertRaises(ValueError):self.engine.update(ident,self.pcm,16000,6)
        data=json.loads((self.root/'resultados/directo_local'/(ident+'.json')).read_text(encoding='utf-8'))
        self.assertTrue(data['finished']);self.assertFalse(data['audio_saved_by_server'])
        self.assertNotIn('tracker',data);self.assertEqual(len(data['updates']),2)

    def test_stale_and_concurrent_windows_cannot_move_tracker(self):
        ident=self.engine.start('lectura_01.txt')['id'];self.engine.update(ident,self.pcm,16000,2)
        with self.assertRaises(ValueError):self.engine.update(ident,self.pcm,16000,2)
        self.engine.lock.acquire()
        try:
            with self.assertRaises(ValueError):self.engine.update(ident,self.pcm,16000,4)
        finally:self.engine.lock.release()
        self.assertEqual(len(self.engine.sessions[ident]['updates']),1)

    def test_resampling_retains_window_duration_and_offset(self):
        data=np.zeros(48000*3,dtype='<f4').tobytes()
        samples,start=pcm_window(data,48000,12)
        self.assertEqual(len(samples),48000);self.assertEqual(start,9)

    def test_untrusted_audio_and_story_paths_rejected(self):
        for rate,end,data in [(16000,1,self.pcm),(16000,2,b'x'),(16000,2,np.array([np.nan],dtype='<f4').tobytes()),(16001,2,self.pcm)]:
            with self.assertRaises(ValueError):pcm_window(data,rate,end)
        with self.assertRaises(ValueError):self.engine.start('../../secreto.txt')

    def test_browser_metrics_do_not_create_automatic_accuracy_scores(self):
        ident=self.engine.start('lectura_01.txt')['id'];self.engine.update(ident,self.pcm,16000,2)
        self.engine.event(dict(id=ident,kind='render',index=0,request_roundtrip_ms=600,estimated_cut_age_at_render_ms=700))
        self.engine.event(dict(id=ident,kind='capture',settings=dict(sampleRate=16000,deviceId='privado')))
        s=self.engine.sessions[ident]
        self.assertNotIn('deviceId',s['capture_settings']);self.assertNotIn('accuracy',s)
        self.assertEqual(s['updates'][0]['browser']['request_roundtrip_ms'],600)

    def test_fast_configuration_is_persisted_and_rejects_oversized_window(self):
        s=self.engine.start('lectura_01.txt',window=4,step=.5)
        self.assertEqual(s['window_seconds'],4);self.assertEqual(s['requested_step_seconds'],.5)
        self.engine.update(s['id'],self.pcm,16000,2)
        too_long=np.zeros(5*16000,dtype='<f4').tobytes()
        with self.assertRaises(ValueError):self.engine.update(s['id'],too_long,16000,6)
        self.assertEqual(len(self.engine.sessions[s['id']]['updates']),1)

    def test_invalid_cadence_is_rejected_before_opening_session(self):
        for window,step in [(4,0),(3,.5),(8,float('nan')),(True,1)]:
            with self.assertRaises(ValueError):self.engine.start('lectura_01.txt',window=window,step=step)
        self.assertEqual(len(self.engine.sessions),0)

    def test_piggyback_metrics_and_final_render_are_saved(self):
        s=self.engine.start('lectura_01.txt',window=4,step=.25,client_profile=2)
        self.assertEqual(self.engine.sessions[s['id']]['capture_block_samples'],512)
        self.engine.update(s['id'],self.pcm,16000,2)
        ack=dict(id=s['id'],kind='render',index=0,request_roundtrip_ms=300,estimated_cut_age_at_render_ms=350)
        self.engine.update(s['id'],self.pcm,16000,4,render=ack)
        self.assertEqual(self.engine.sessions[s['id']]['updates'][0]['browser']['request_roundtrip_ms'],300)
        ack['index']=1;self.engine.event(dict(id=s['id'],kind='finish',render=ack))
        data=json.loads((self.root/'resultados/directo_local'/(s['id']+'.json')).read_text(encoding='utf-8'))
        self.assertTrue(data['finished']);self.assertIn('browser',data['updates'][-1])

    def test_piggyback_cannot_relabel_other_session(self):
        s=self.engine.start('lectura_01.txt');self.engine.update(s['id'],self.pcm,16000,2)
        with self.assertRaises(ValueError):
            self.engine.update(s['id'],self.pcm,16000,4,render=dict(id='otro',kind='render',index=0))
        self.assertEqual(len(self.engine.sessions[s['id']]['updates']),1)

    def test_pair_mode_is_metadata_and_does_not_move_recognized_position(self):
        s=self.engine.start('lectura_01.txt',guide_words=2,step=.125)
        self.assertEqual(s['guide_words'],2)
        self.assertEqual(s['requested_step_seconds'],.125)
        r=self.engine.update(s['id'],self.pcm,16000,2)
        self.assertEqual(r['position'],3)
        self.assertEqual(self.engine.sessions[s['id']]['visual_guide']['policy'],'sliding_next_words')
        self.engine.event(dict(id=s['id'],kind='finish'))
        with self.assertRaises(ValueError):self.engine.start('lectura_01.txt',guide_words=3)


if __name__=='__main__':unittest.main()
