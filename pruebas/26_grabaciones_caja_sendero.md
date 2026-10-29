# La caja del sendero: tanda de seis lecturas

26/10/2026. Preparación de nuevas grabaciones para ampliar el dataset e investigar fidelidad literal. Texto nuevo de 98 palabras en datos/textos/lectura_04.txt; lectura_03.txt ya existía y se conserva. Consignas estructuradas en datos/textos/lectura_04_tomas.json. Estado inicial: preparación de la tanda; ejecución y confirmación documentadas al final.

## Grabar

Desde la carpeta del proyecto, ejecutar una sola vez:

```powershell
.\.venv\Scripts\python.exe -u -m scripts.grabar_tanda
```

El programa muestra cada consigna y el cuento, espera Enter y graba la toma. Al guardarla presenta la siguiente; no inicia el siguiente audio hasta otro Enter. Reutiliza scripts/grabar.py: mismo micrófono predeterminado, WAV mono PCM16 a frecuencia nativa y catálogo con huella, cuento y nombre descriptivo real del archivo. No se ejecuta ASR ni se sube contenido.

Lee una vez todo el cuento en cada toma. No pronuncies las consignas ni el título. Al acabar permanece sin hablar hasta que aparezca Guardado; los segundos restantes son cola final conservada en el original. Ctrl+C interrumpe, no guarda anticipadamente. Las duraciones dan margen; si falta tiempo, no aceleres para compensarlo: comunica la toma incompleta. Conserva micrófono, distancia y ambiente lo más parecidos posible. Si hay ruido, comunícalo; no se presupone ausencia de ruido.

| Toma | Duración fija | Consigna |
|---|---:|---|
| 1. Normal | 90 s | Ritmo habitual, sin errores deliberados. |
| 2. Palabras repetidas | 100 s | «una una pequeña caja», «Clara Clara abrió», «Mateo Mateo probó» y «junto junto al puente» en la última frase. |
| 3. Intentos parciales | 120 s | «pe- pe- pequeña», «des- des- descubrieron», «regres- re- regresar». Guion significa cortar la palabra. |
| 4. Omisiones/sustituciones | 90 s | Omitir «madera» y «viejo»; decir «pluma roja» y «un parque» en lugar de «pluma azul» y «un jardín». No autocorregir. |
| 5. Pausa y continuación | 120 s | Tras «y un papel doblado», callar unos 8 s; seguir por «Clara abrió» y terminar, sin repetir la frase anterior. |
| 6. Mixta libre | 150 s | Repeticiones, intentos parciales y velocidades variados libremente; terminar el cuento. No hace falta trabarse en cada palabra. |

Tiempo total de captura: 670 s (11 min 10 s), más la preparación entre tomas. Son seis lecturas distintas; repetir el cómputo posteriormente no aumenta ese número. Los nombres son consignas y no confirman lo que realmente se pronunció. El adulto simula dificultades: no son datos clínicos ni una muestra de lectores infantiles.

Para ver las consignas sin grabar:

```powershell
.\.venv\Scripts\python.exe -m scripts.grabar_tanda --listar
```

Para continuar, por ejemplo, desde la cuarta toma:

```powershell
.\.venv\Scripts\python.exe -u -m scripts.grabar_tanda --desde 4
```

No repitas las tomas ya guardadas salvo que quieras otra grabación independiente. Si se repite un nombre el grabador añade un sufijo; no sobrescribe el WAV anterior. Se puede indicar --hasta para limitar la tanda, --ambiente para describir condiciones reales y --dispositivo para elegir otro micrófono.

## Revisión y comparación posterior

Mantener ajustes fijados al reconocer la tanda, comparar transcripción habitual/literal y variante de final VAD, con tiempos y recursos registrados. No usar el cuento como si fuera transcripción literal de los errores. Las consignas son hipótesis de referencia; confirmar por escucha antes de contar intentos, omisiones o sustituciones. Conservar WAV originales y salidas brutas separadas de cualquier corrección humana.

Usar 1–4 para analizar y desarrollar cambios. Reservar 5–6 para comprobar cambios posteriores sin usarlos para decidir las reglas; esta intención está en el plan, no asignada aún a WAV inexistentes. Si sus resultados se utilizan para ajustar, pasan a desarrollo y habrá que grabar una nueva validación. Mismo lector/texto/dispositivo: esta reserva no demuestra generalización a otras personas o textos.


## Tanda grabada y confirmación del lector

26/10/2026. Se verifican seis WAV de 90/100/120/90/120/150 s, mono PCM16 44.100 Hz y 670 s en total, con huellas coincidentes con el catálogo. El lector confirma las consignas y describe en la sexta confusiones/autocorrecciones, recuerda «descubrieron» y después «encontraron una caja...», otra autocorrección no recordada, repeticiones parciales y velocidades lentas/rápidas. No se interpreta esa descripción como transcripción exacta ni se inventan tiempos o la segunda corrección. Declaración y huellas en datos/anotaciones/lectura_04_tanda_confirmacion.json; ambiente no descrito.

Se fija únicamente este cuento mediante --cuento, conservando cobertura e integridad del resto del catálogo. Preparación del nuevo lote en resultados/literalidad/20261026_081747_630720_UTC, sin repetir los 17 WAV anteriores. Mismos modelos y trabajador que en el contraste anterior: motor actual sobre audio completo, candidato literal completo y contraste posterior del mismo candidato con límite final VAD. Ningún cuento o consigna se entrega como prompt. Salidas separadas y tiempos/CPU/RAM/GPU global según el monitor existente. Tomas 1–4 en desarrollo y 5–6 reservadas para validar cambios posteriores; no se ajustan reglas con sus salidas. Reconocerlas con configuración ya fijada no implica usarlas para diseñar un cambio.

## Comparación terminada

Dieciocho transcripciones nuevas, seis por configuración. Resultados y límites en resultados/literalidad/20261026_081747_630720_UTC/revision_inicial.md. Variante VAD en resultados/literalidad/20261026_082404_701027_cola_vad_UTC. Visores 8780 (actual/literal) y 8781 (literal/VAD), pendientes de revisión compartida; no se publica ni activa la variante.

## Actualización del control de grabación

26/10/2026, tras la tanda inicial: grabar_tanda activa ahora --parar-con-enter. Enter inicia; otro Enter termina y guarda; los tiempos del plan son máximos. La duración real se registra en el catálogo y no se rellena con silencio. Las duraciones históricas descritas arriba corresponden a la tanda ya grabada, que se conserva intacta.
