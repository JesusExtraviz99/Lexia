"""Diagnóstico sin cambios de reglas: búsqueda local y recuperación global en casos sintéticos."""
import json

from scripts.alinear import tokens
from scripts.comparar_combinacion import far_rereading_check
from scripts.comparar_seguidores import CombinedTracker, replay
from scripts.seguir import locate


def timed(text, start):
    return [{'word': w, 'start': start + i, 'end': start + i + 1}
            for i, w in enumerate(tokens(text))]


STORY = tokens('mirando sus alas después volvieron a casa y dibujaron la mariposa en un cuaderno')
PREFIX = [timed('mirando sus alas', 0), timed('Después', 3),
          timed('y dibujaron la mariposa en un cuaderno', 8), timed('en un jugaderno', 12)]


def diagnose(hypotheses):
    """Instrumenta el estado y verifica que coincide con la reproducción existente."""
    tracker = CombinedTracker(STORY)
    for hypothesis in PREFIX:
        tracker.update_timed(hypothesis)
    if tracker.position != 14:
        raise ValueError('La secuencia de partida ya no reproduce el límite diagnosticado.')
    previous = [w['word'] for w in PREFIX[-1]]
    rows = []
    for step, hypothesis in enumerate(hypotheses, 1):
        heard = [w['word'] for w in hypothesis]
        changed = heard != previous
        old, failures = tracker.position, tracker.failures
        local = locate(STORY, heard, old)
        # Consulta adicional solo para explicar qué encontraría la búsqueda global;
        # no alimenta al Tracker ni modifica sus contadores/candidatos.
        global_evidence = locate(STORY, heard, old, global_search=True)
        if changed:
            state = tracker.update_timed(hypothesis)
        else:
            state = {'position': old, 'mode': 'hipotesis_sin_cambios'}
        rows.append({'step': step, 'text': ' '.join(heard), 'text_changed': changed,
                     'local_window': local.get('window_indices'),
                     'local_position': local['position'], 'local_matches': local.get('exact_matches'),
                     'global_diagnostic_position': global_evidence['position'],
                     'global_search_triggered': changed and local['position'] is None and failures + 1 >= 2,
                     'failures': tracker.failures, 'pending_candidate': tracker.recovery_candidate,
                     'position': state['position'], 'mode': state['mode']})
        previous = heard
    data = {'story_words': STORY, 'updates': [{'hypothesis': h} for h in PREFIX + hypotheses]}
    reproduced = replay(data, CombinedTracker)['updates'][-len(hypotheses):]
    if [(r['position'], r['mode']) for r in rows] != [(r['position'], r['mode']) for r in reproduced]:
        raise ValueError('El diagnóstico no coincide con la reproducción habitual.')
    return rows


def scenarios():
    return [
        ('A. Texto y tiempos repetidos',
         [timed('mirando sus alas', 20) for _ in range(3)]),
        ('B. Mismo texto, tiempos posteriores',
         [timed('mirando sus alas', 20 + 2 * i) for i in range(3)]),
        ('C. La frase va creciendo',
         [timed(text, 20) for text in ['mirando sus alas', 'mirando sus alas después',
                                      'mirando sus alas después volvieron']]),
        ('D. Textos distintos respaldan el mismo candidato',
         [timed(text, 20) for text in ['mirando sus alas', 'mirando sus sus alas',
                                      'mirando mirando sus alas']]),
    ]


def main():
    print('DIAGNOSTICO DE RECUPERACION - sin modificar reglas')
    print('Casos sinteticos: no son nuevas grabaciones, reconocimiento ni medidas de latencia.')
    print('El comando no escribe archivos. Instrumenta el seguidor combinado y comprueba que coincide con replay.')
    print('\nPUNTO DE PARTIDA')
    print('Posicion 14: cuaderno. La busqueda local abarca 3-14: empieza en alas.')
    print('Frase de vuelta: mirando(1) sus(2) alas(3). Localmente solo queda alas.')
    first = locate(STORY, tokens('mirando sus alas'), previous=14)
    global_first = locate(STORY, tokens('mirando sus alas'), previous=14, global_search=True)
    print(f"Busqueda local: {first['exact_matches']}/3 coincidencias; candidato {first['position']}.")
    print(f"Busqueda en todo el cuento: {global_first['exact_matches']}/3 coincidencias; candidato {global_first['position']}.")
    print('La consulta global mostrada para diagnostico no obliga al algoritmo a ejecutarla o aceptarla.')
    print('\nREGLAS DE RECUPERACION ACTUALES')
    print('1. El texto debe cambiar para que se procese una nueva hipotesis.')
    print('2. Tras dos fallos locales se empieza a buscar en todo el cuento.')
    print('3. El candidato global debe coincidir con el candidato pendiente de otra actualizacion procesada.')
    print('4. Un acierto local puede recuperar directamente y reinicia el contador de fallos.')
    print('5. Los retrocesos aceptados por la variante pasan ademas el filtro temporal.')
    for title, hypotheses in scenarios():
        print(f'\n{title}')
        print('Paso | Texto distinto | Local | Global diagnostico | Global ejecutada | Fallos | Pendiente | Posicion | Modo')
        for row in diagnose(hypotheses):
            print(f"{row['step']} | {'si' if row['text_changed'] else 'no'} | {row['local_position']} | {row['global_diagnostic_position']} | {'si' if row['global_search_triggered'] else 'no'} | {row['failures']} | {row['pending_candidate']} | {row['position']} | {row['mode']}")
            print(f"  Texto: {row['text']}")
    print('\nCONTROL DEL EJEMPLO ANTERIOR')
    print(json.dumps(far_rereading_check()['positions_after_rereading'], ensure_ascii=False))
    print('\nCONCLUSION DEL DIAGNOSTICO')
    print('A/B: el texto identico no permite acumular fallos ni confirmar recuperacion; sigue en 14 tras estas tres propuestas.')
    print('C: recupera localmente en el paso 3, posicion 5, cuando hay suficiente frase dentro de su ventana.')
    print('D: recupera globalmente en el paso 3, posicion 3, tras dos candidatos globales iguales con textos distintos.')
    print('No hay audio real ni tiempos de palabras humanos en estos casos: los pasos no equivalen a segundos de demora.')
    print('Diagnostico solamente. Ninguna regla se ha corregido o activado con este comando.')


if __name__ == '__main__':
    main()
