"""Conservar catálogo completo privado y exportar solo lector_01 para Git."""
from copy import deepcopy
import json
from scripts.catalogo import ROOT, read_catalog
from scripts.archivos import write_text_atomic


def public_catalog(catalog):
    result = deepcopy(catalog)
    result['recordings'] = [r for r in result['recordings']
                            if r.get('speaker_id') in ('lector_01', 'adulto_01')]
    result['publication_scope'] = 'Solo grabaciones autorizadas de lector_01; el catálogo completo se conserva localmente fuera de Git.'
    return result


def main():
    catalog = read_catalog()
    private = ROOT/'datos/referencias/catalogo_local.json'
    write_text_atomic(private, json.dumps(catalog, ensure_ascii=False, indent=2)+'\n')
    public = public_catalog(catalog)
    write_text_atomic(ROOT/'datos/referencias/catalogo.json', json.dumps(public, ensure_ascii=False, indent=2)+'\n')
    print(f'Catálogo local: {len(catalog["recordings"])} entradas. Público: {len(public["recordings"])} entradas del lector original.')


if __name__ == '__main__':
    main()
