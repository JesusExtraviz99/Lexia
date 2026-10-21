# Diagnóstico de la recuperación de una relectura lejana

Fecha: 19/10/2026. Análisis de las reglas existentes, sin corrección nueva. Casos sintéticos; pendiente de comprobación compartida del usuario.

## Comprobar en el ordenador del usuario

```powershell
.\.venv\Scripts\python.exe -m scripts.diagnosticar_recuperacion
```

El comando imprime cuatro secuencias y no escribe archivos, no ejecuta ASR ni activa el micrófono. La instrumentación verifica sus posiciones y modos frente a replay en cada secuencia. No se modifica el seguidor original ni las variantes anteriores.

## Hallazgo

Con posición previa 14, la ventana local del ejemplo abarca las palabras 3–14. La relectura mirando sus alas ocupa 1–3, por lo que solo alas queda dentro de la ventana: una coincidencia de tres, insuficiente. Una búsqueda global encuentra las tres coincidencias y posición 3.

La búsqueda global existe, pero no se usa ni acepta inmediatamente:

1. La política de reproducción solo procesa una actualización si cambia el texto de la hipótesis. Los cambios exclusivamente temporales no cuentan.
2. Tracker necesita dos fallos locales procesados para consultar el cuento completo.
3. El primer candidato global se guarda pendiente. Para aceptarlo, otra actualización procesada debe proponer el mismo índice global.
4. Un candidato local aceptado puede resolver el problema antes y reinicia el contador de fallos.
5. En la variante temporal o combinada, un retroceso aceptado debe además superar la comprobación de respaldo temporal posterior.

La columna Global diagnóstico se calcula adicionalmente para explicar qué encontraría la búsqueda global; no alimenta el seguimiento. Global ejecutada distingue cuándo el algoritmo sí la consulta. None significa que esa búsqueda no acepta candidato. El modo local por sí solo no significa que se haya aceptado una nueva posición.

## Cuatro secuencias sintéticas, mismo punto de partida

| Secuencia | Resultado tras tres propuestas | Explicación |
|---|---|---|
| A. Texto y tiempos repetidos | 14 → 14 → 14 | Primer fallo local; las dos propuestas siguientes no se procesan porque el texto es idéntico. |
| B. Texto idéntico con tiempos posteriores | 14 → 14 → 14 | La política compara solo texto; esos timestamps posteriores no llegan al filtro temporal. |
| C. Frase creciente: mirando sus alas / … después / … después volvieron | 14 → 14 → 5 | El segundo paso guarda candidato global 4. En el tercero ya hay suficientes coincidencias locales y recupera por búsqueda local. |
| D. Textos distintos con candidato global 3 | 14 → 14 → 3 | En el segundo paso guarda 3; el tercero confirma 3 y acepta recuperación global con respaldo temporal posterior al apoyo anterior. |

En D se construyen dos variaciones con palabras repetidas para analizar la confirmación: mirando sus sus alas y mirando mirando sus alas. No son lecturas del usuario ni salidas medidas del ASR. Dos textos distintos tampoco demuestran que se hayan analizado dos eventos de habla independientes.

Los pasos son propuestas sintéticas, no segundos de latencia real. La frase creciente muestra que no es correcto afirmar que el algoritmo nunca se recupera: depende de la secuencia recibida. A/B muestran que puede quedarse esperando aunque una consulta global encuentre la frase.

## Decisión tras este análisis

Conservar las reglas y esperar la comprobación compartida. La siguiente variante a estudiar puede adelantar la recuperación cuando la búsqueda local falla y existe una coincidencia global especialmente fuerte, inequívoca y con respaldo temporal posterior. Deberá contrastarse con revisiones del mismo audio, frases repetidas en el cuento y el resto de casos antes de adoptarla.

No ampliar la ventana solo para que quepa el ejemplo ni tratar texto repetido como confirmaciones independientes. No se fija todavía un umbral nuevo ni se modifica la política de texto idéntico en este diagnóstico.
