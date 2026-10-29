# Texto largo: El recuerdo del banco azul

26/10/2026. Se prepara lectura_05.txt, texto original nuevo de 250 palabras en cinco párrafos, para ampliar la duración/contexto respecto a los anteriores. Plan lectura_05_tomas.json: tres controles de ritmo y cinco pruebas difíciles. Sin alterar cuentos o grabaciones previas. Un adulto y dificultades simuladas: exploración de desarrollo, no prueba final independiente.

```powershell
.\.venv\Scripts\python.exe -u -m scripts.grabar_tanda --plan datos/textos/lectura_05_tomas.json
```

Enter inicia; otro Enter termina y guarda. El siguiente audio espera otra pulsación. Los tiempos solo son máximos. Se amplía el límite permitido del grabador/tanda a 600 s para dar margen a lecturas lentas largas; no se amplían ni rellenan WAV anteriores. La toma lenta permite 480 s, sin obligación de agotarlos. No usar Ctrl+C para guardar. No decir título ni consignas.

| Toma | Máximo (s) | Consigna |
|---|---:|---|
| 01 | 240 | Normal completa. |
| 02 | 480 | Lenta completa sin errores deliberados. |
| 03 | 180 | Rápida e inteligible. |
| 04 | 360 | Repetición de mochila e intentos en brújula, fotografía, descubrieron y exposición final. |
| 05 | 360 | Omitir antiguos/amarillo; sustituir campana→cámara y banco azul→verde, sin autocorregir. |
| 06 | 360 | Pausa aproximada de 15 s tras segundo párrafo y continuación. |
| 07 | 420 | Texto completo y relectura solo del tercer párrafo; termina en ventana. |
| 08 | 480 | Mezcla libre distribuida por párrafos. |

Máximos acumulados 2.880 s (48 min), no duración esperada de la tanda. La parada manual registra duración real. Se puede dividir con --hasta 4 y retomar con --desde 5 conservando el mismo --plan. Nombres reales Biblioteca 01–08, cuento y fecha. --ambiente describe condiciones reales; --lector distingue voces. No activar micrófono al preparar/listar.

La puerta estaba cerrada aparece dos veces en lugares distintos del cuento: ambas son texto legítimo. Fotografía y exposición también se repiten legítimamente; las consignas precisan dónde introducir intentos. Las pausas entre párrafos y la pausa de 15 s no tienen límites humanos medidos por el mero hecho de pedirlas. La relectura 07 termina en posición anterior al final; llegar a exposición no basta para considerar correcto el seguimiento de toda esa toma.

## Comparación posterior

Mantener grabación original y cronología; el literal final se ejecutará bajo demanda una vez el usuario cierre la recogida. No iniciar ASR al preparar esta tanda ni tras cada WAV. Al procesar, congelar selección/configuraciones/huellas y comparar los mismos audios nuevos sin repetir los ya reconocidos salvo contraste explícito. El modelo literal tiene bloques internos, por lo que un texto largo no implica reconocimiento de todo el WAV en una sola ventana. Los recursos y tiempos se medirán; no se presupone crecimiento lineal ni conservación perfecta entre bloques.

Priorizar comparación de intentos repartidos por párrafos, continuidad tras pausa y recuperación lejana. Conservar controles fluidos, omisiones/sustituciones pronunciadas y salidas brutas; no usar el cuento como transcripción de los errores ni contar hipótesis solapadas como nuevos intentos. Referencia por escucha pendiente. Se mantienen las reservas anteriores; estas nuevas tomas se prevén de desarrollo. Sin publicación automática.


## Recogida completada

26/10/2026. El lector comunica Tanda terminada. Verificados ocho WAV, 1.351,969 s de archivo (22 min 31,97 s). Duraciones reales 130,344 / 339,177 / 75,785 / 155,485 / 112,518 / 123,157 / 126,248 / 289,255 s. Referencia descriptiva con huellas: datos/anotaciones/lectura_05_tanda_confirmacion.json; consignas aún pendientes de revisión por evento, sin tiempos humanos. Total disponible 49 audios, cinco textos y 3.921,973 s con silencios, un lector. Reconocimiento pendiente de cierre de la recogida por el usuario; sin publicación o activación automática.
