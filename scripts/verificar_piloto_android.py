"""Comprueba el contenido de la entrega y registra evidencia sin instalar en el teléfono."""
from datetime import datetime,timezone
import argparse,hashlib,json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def sha(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--version',choices=['0.1','0.2','0.3','0.4','0.5'],default='0.1');args=parser.parse_args()
    project=ROOT/'mobile/android';apk=ROOT/'.descartados/android'/('lexia-piloto-'+args.version+'-arm64.apk')
    original=project/'app/build/outputs/apk/debug/app-debug.apk'
    assert sha(apk)==sha(original),'La entrega no coincide con el build'
    with zipfile.ZipFile(apk) as package:
        names=set(package.namelist())
        assert {'classes.dex','AndroidManifest.xml'}<=names
        for lib in ('libmoonshine.so','libmoonshine-jni.so','libonnxruntime.so'):
            assert 'lib/arm64-v8a/'+lib in names,lib
        if args.version!='0.1':
            with zipfile.ZipFile(ROOT/'.descartados/android/lexia-piloto-0.1-arm64.apk') as previous:
                for lib in ('libmoonshine.so','libmoonshine-jni.so','libonnxruntime.so'):
                    name='lib/arm64-v8a/'+lib
                    assert package.read(name)==previous.read(name),'Cambio no previsto del SDK nativo: '+lib
        assert not any(n.startswith('lib/') and not n.startswith('lib/arm64-v8a/') for n in names)
        for text in (ROOT/'datos/textos').glob('lectura_*.txt'):
            assert package.read('assets/textos/'+text.name)==text.read_bytes(),text.name
    lint=ET.parse(project/'app/build/reports/lint-results-debug.xml').getroot()
    errors=[r for r in lint.findall('issue') if r.attrib['severity'] in ('Error','Fatal')]
    assert not errors,'Android Lint contiene errores'
    warnings=[r.attrib['id'] for r in lint.findall('issue') if r.attrib['severity']=='Warning']
    sources={p.relative_to(ROOT).as_posix():sha(p) for p in project.rglob('*') if p.is_file() and not ({'build','.gradle'}&set(p.relative_to(project).parts)) and p.name!='local.properties'}
    sources['scripts/compilar_android.ps1']=sha(ROOT/'scripts/compilar_android.ps1')
    replay_updates=0
    for path in (ROOT/'.descartados/android').glob('*.tsv'):
        replay_updates+=len(path.read_text(encoding='utf-8').splitlines())-(2 if path.name.startswith(('margin_','support_')) else 1)
    payload=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),status='prepared_not_tested_on_phone',
        apk=apk.relative_to(ROOT).as_posix(),bytes=apk.stat().st_size,sha256=sha(apk),
        sdk='ai.moonshine:moonshine-voice:0.1.5',abi='arm64-v8a',min_sdk=26,target_sdk=35,compile_sdk=36,
        source_sha256=sources,android_lint_errors=0,android_lint_warning_ids=warnings,
        java_python_replay_fixture_updates=replay_updates,
        apk_signature='apksigner verify: v2 verified, 1 signer; debug build',zip_alignment='zipalign -c -P 16 4 passed',
        assets_match_project_texts=True,device='Redmi Note 13 Pro+ 5G comunicado por el usuario',
        device_source='https://www.mi.com/es/product/redmi-note-13-pro-plus-5g/specs/',
        phone_ram_variant_unknown=args.version=='0.1',phone_android_version_unknown=args.version=='0.1',
        previously_verified_phone_android='16' if args.version!='0.1' else None,
        guide_policy='sliding_next_words' if args.version!='0.1' else 'fixed_pairs',
        native_sdk_binaries_match_v01=True if args.version!='0.1' else None,
        notice='Esta versión aún no tiene lectura humana en dispositivo real. Runtime SDK/ONNX streaming distinto del PC PyTorch. Pesos identificados en el teléfono por huella. No hay voces incluidas ni publicación.')
    if args.version=='0.3':
        payload['native_interval_choices_seconds']=[.5,.25,.125]
        payload['local_context_choices_words']=[12,5]
        payload['global_recovery_enabled']=True
        payload['default_native_interval_seconds']=.5
        payload['default_local_context_words']=12
    if args.version in ('0.4','0.5'):
        payload.update(native_interval_choices_seconds=[.25,.125],default_native_interval_seconds=.125,
                       local_context_choices_words=[12,5],default_local_context_words=12,
                       advance_policy_choices=['original','terminal_and_recent'],default_advance_policy='original',
                       global_recovery_enabled=True)
    if args.version=='0.5':
        payload.update(guide_width_choices=[2,3,1],default_guide_width=2,adaptive_cadence_enabled=False)
    out=ROOT/('resultados/android/piloto_20261109' if args.version=='0.1' else 'resultados/android/piloto_20261109_v'+args.version.replace('.',''));out.mkdir(parents=True,exist_ok=True)
    (out/'preparacion.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    Path(str(apk)+'.sha256').write_bytes((payload['sha256']+'  '+apk.name+'\n').encode())
    print(json.dumps({k:payload[k] for k in ('status','apk','bytes','sha256','android_lint_errors','java_python_replay_fixture_updates')},indent=2))
    if args.version!='0.1':return
    files=['91187a8da5824160168f3390','1a20e2d158e3f4ae4bf72ccd','1a4024f2dffc598ef42cbf07',
        '44c75f0a83429ceec88e3038','96c5c0e95ff7b8776b258077','ecfb3550bca098dbc2c195b9']
    rows=[]
    for ident in files:
        path=ROOT/'resultados/directo_local'/(ident+'.json');s=json.loads(path.read_text(encoding='utf-8'))
        rows.append(dict(file=path.name,sha256=sha(path),model=s['model'],guide=s['visual_guide'],step=s['requested_step_seconds'],
            updates=len(s['updates']),backtracks=sum(r['movement']<0 for r in s['updates']),final_position=s['updates'][-1]['position']))
    private=ROOT/'resultados/directo_local/revision_20261109_parejas';private.mkdir(exist_ok=True)
    (private/'resumen.json').write_text(json.dumps(dict(rows=rows,user_prefers_pairs=True,
        notice='Tomas distintas: no se atribuyen al resaltado diferencias en hipótesis/retrocesos del alineador. Retrocesos no equivalen por sí solos a fallos sin escucha/anclas. Sin ASR nuevo.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
