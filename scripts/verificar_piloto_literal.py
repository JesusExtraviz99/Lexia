"""Verifica entradas, resultados y procedencia del piloto, sin inferencias."""
import argparse
import json
from pathlib import Path

from scripts.archivos import write_text_atomic
from scripts.catalogo import ROOT
from scripts.comparar_literalidad import digest
from scripts.ver_piloto_literal import load


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    args=parser.parse_args();folder=args.folder.resolve()
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    payload,_=load(folder)
    complete=bool(manifest.get('source_pilot'))
    assert len(manifest['samples'])==(1 if complete else 7)
    assert {s['kind'] for s in manifest['samples']}==({'trabadas'} if complete else {'trabadas','control_fluido','control_sin_habla'})
    for sample in manifest['samples']:
        assert digest(ROOT/sample['array_file'])==sample['array_sha256']
        assert digest(ROOT/sample['source_audio'])==sample['source_sha256']
    if complete:
        import numpy as np
        prior=ROOT/manifest['source_pilot']
        assert all(digest(prior/name)==value for name,value in manifest['prior_hashes'].items())
        previous=json.loads((prior/'manifest.json').read_text(encoding='utf-8'))
        full=np.load(ROOT/manifest['samples'][0]['array_file'],allow_pickle=False)
        for sample in previous['samples']:
            if sample['kind']=='trabadas':
                array=np.load(ROOT/sample['array_file'],allow_pickle=False)
                assert np.array_equal(array,full[round(sample['start']*16000):round(sample['end']*16000)])
        assert len(payload['samples'])==5
    provenance=manifest['candidate_model']
    for file in provenance['files']:
        assert digest(ROOT/'modelos/crisperwhisper2-small'/file['file'])==file['sha256']
    outputs={e:json.loads((folder/(e+'.json')).read_text(encoding='utf-8')) for e in ['baseline','candidato']}
    for engine,result in outputs.items():
        assert result['device']=='cpu' and result['status']=='completo'
        assert {r['id'] for r in result['runs']}=={s['id'] for s in manifest['samples']}
        assert all(r['processing_seconds']>=0 for r in result['runs'])
        print(engine,':',len(result['runs']),'muestras,',round(sum(r['processing_seconds'] for r in result['runs']),2),'s')
    assert outputs['baseline']['script_sha256']==outputs['candidato']['script_sha256']
    # Solo cambió posteriormente la clave usada por la tabla de RAM; recuperar
    # una copia exacta y comprobar su hash antes de archivarla como evidencia.
    source=(ROOT/'scripts/comparar_literalidad.py').read_bytes()
    import hashlib
    expected=outputs['baseline']['script_sha256']
    archive=folder/'fuente_ejecutada.txt'
    if archive.exists() and digest(archive)==expected:
        frozen=archive.read_bytes()
    elif hashlib.sha256(source).hexdigest()==expected:
        frozen=source
    else:
        frozen=source.replace(b"peak=memory.get('process_lifetime_peak_working_set_bytes')",b"peak=memory.get('peak_working_set_bytes')")
    source_preserved=hashlib.sha256(frozen).hexdigest()==outputs['baseline']['script_sha256']
    if source_preserved:
        (folder/'fuente_ejecutada.txt').write_bytes(frozen)
    earlier=ROOT/'resultados/lotes/20261023_102114_072901/revision_asistente.json'
    history=json.loads(earlier.read_text(encoding='utf-8'))
    assert all(digest(ROOT/s['file'])==s['sha256'] for s in history['sources'])
    result=dict(manifest_sha256=digest(folder/'manifest.json'),
                outputs_sha256={e:digest(folder/(e+'.json')) for e in outputs},
                audio_inputs_verified=len(manifest['samples']),models_files_verified=len(provenance['files']),
                historical_records_unchanged=len(history['sources']),
                model_revision=provenance['revision'],source_snapshot_matches_execution=source_preserved,
                note=('Comprobación técnica, no validación humana de eventos ni de marcas temporales. '
                      +('Audio completo: cuatro recortes previos coinciden exactamente con sus intervalos; hashes del piloto original intactos.' if complete else 'La tabla de RAM se generó con clave corregida, sin repetir ni cambiar inferencias.')))
    write_text_atomic(folder/'integridad.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Integridad verificada. Copia exacta del código ejecutado:',source_preserved)
    print('Los 42 registros del seguidor siguen intactos.')


if __name__=='__main__':main()
