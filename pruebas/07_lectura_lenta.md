# Prueba 07: lectura lenta con ventanas de 4 y 8 segundos

Fecha: 16/10/2026. Ejecutada por el usuario; salida y registros locales revisados. El usuario autoriza su publicación con el WAV y resultados. Sin cambios de código.

Audio: `datos/audio/lectura_20261016_095108_269618.wav`, duración 90 s. Tres rondas por ventana, bloque de 2 s, Whisper small, CPU int8, VAD y seguidor sin cambios. Registros en `resultados/comparaciones/20261016_095252_869489/`.

## Resultados

| Ventana | Inferencia total media (s) | Rango entre rondas (s) | Inferencias >2 s | Media de cola máxima simulada (s) | Posición final |
|---|---:|---|---:|---:|---|
| 4 s | 68,74 | 67,18–71,14 | 9/135 | 2,03 | 53: mariposa, en las tres rondas |
| 8 s | 93,29 | 87,79–98,30 | 4/135 | 22,72 | 55: un, en las tres rondas |

Estos tiempos excluyen carga del modelo. Las colas son simuladas y las posiciones se asocian a cortes de audio disponible, no a tiempos de pantalla. Falta referencia humana temporal y transcripción literal de esta lectura.

## Hallazgos de seguimiento

- Ventana 4: al corte de 62 s solo devuelve Después, insuficiente para la regla de dos coincidencias. Al corte de 64 s devuelve Pues volvieron, con una sola coincidencia de dos tokens, y mantiene alas (45). Recupera casa (49) al corte de 66 s.
- Ventana 4: desde el corte de 72 s permanece en mariposa (53); no alcanza cuaderno en ninguna ronda. Hay hipótesis incompatibles o evidencia insuficiente en los últimos fragmentos.
- Ventana 8: alcanza cuaderno (56) al corte de 78 s. Al corte de 80 s la hipótesis cambia a en un jugaderno; se aceptan las dos coincidencias en un y se retrocede a un (55). Esa posición se conserva hasta el final. Sucede en las tres rondas.
- No se ha confirmado por escucha una relectura real al final. El retroceso está asociado a una revisión del ASR; no debe atribuirse automáticamente al lector.

## Hallazgos de procesamiento

Con ventana 8, el intervalo acústico 2–10 s tarda 26,21 / 27,03 / 20,90 s y devuelve una hipótesis vacía en las tres rondas. El pico es reproducible en el mismo intervalo y domina la cola, aunque casi todas las demás inferencias sean rápidas. Los registros actuales no desglosan VAD, decodificación ni posibles reintentos internos: no permiten establecer la causa.

Con ventana 4, aparecen picos menores en los cortes de 58, 62 y 74 s. Tener menos inferencias superiores a 2 s no garantiza menor espera: la magnitud de los excesos importa.

## Salidas ajenas o discrepantes

La ventana 4 devuelve y nos vemos en el próximo vídeo hasta la próxima en el corte de 76 s. Se registra como texto ajeno al cuento y posible alucinación pendiente de escucha; no se atribuye a pájaros ni a una emisión del lector sin revisar este audio concreto. También aparecen fragmentos deformados como Madibosa En, Un jugaderno y Aderno. El resultado final no certifica corrección de pronunciación.

## Consecuencias

La preferencia provisional por 4 s en lecturas anteriores no basta para lectura lenta. Ocho segundos aportan contexto útil para alcanzar el final, pero presentan un pico grave de procesamiento y una regresión posterior. Ninguna configuración supera íntegramente esta prueba.

Conservar esta ejecución como referencia de fallos. Completar la prueba de relectura antes de modificar reglas: necesitamos distinguir un retroceso real de una revisión del ASR, sin imponer un cursor que solo avance. Después investigar el pico del intervalo 2–10 s y opciones de acumulación/adaptación de contexto con comparación controlada. No se aplican ajustes ni se descartan resultados en esta revisión.
