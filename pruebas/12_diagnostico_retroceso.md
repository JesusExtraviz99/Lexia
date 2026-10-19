# Diagnóstico del retroceso después de cuaderno

Fecha: 19/10/2026. Análisis del seguidor original sobre registros existentes; ninguna corrección nueva aplicada. Comprobación del diagnóstico en terminal pendiente del usuario.

## Reproducir desde PowerShell

```powershell
.\.venv\Scripts\python.exe -m scripts.diagnosticar_retroceso
```

Muestra una tabla, el cálculo que acepta el retroceso y un control de las tres rondas. Para ver otra ronda en detalle, añadir --ronda 2 o --ronda 3. El comando solo lee archivos: no graba, no ejecuta reconocimiento, no descarga nada y no guarda cambios.

## Secuencia observada

| Corte de audio | Ventana que se reconoce | Texto ASR | Posición del seguidor |
|---:|---|---|---|
| 78 s | 70–78 s | mariposa en un cuaderno | 56, cuaderno |
| 80 s | 72–80 s | en un jugaderno | Retrocede a 55, un |
| 82 s | 74–82 s | Un jugaderno | Conserva 55 por evidencia insuficiente |
| 84 s | 76–84 s | Aderno | Conserva 55 por evidencia insuficiente |
| 86 s | 78–86 s | Vacío | Conserva 55 |

El mismo paso 56→55 aparece en las tres rondas de ventana 8 s. El diagnóstico reproduce las posiciones, movimientos y modos de los tres registros completos antes de explicar el corte.

## Por qué acepta el retroceso

En el cuento: en / un / cuaderno. En la nueva hipótesis: en / un / jugaderno. Hay dos coincidencias exactas de tres palabras (66,7%) y una edición de tres (33,3%). Se cumplen los requisitos del alineamiento original: al menos dos coincidencias, al menos 60% de coincidencias y como máximo 40% de coste normalizado.

La posición se define como la última palabra coincidente exactamente, que ahora es un (55). Tracker.update acepta ese candidato local directamente y reemplaza la posición 56, sin exigir evidencia adicional de relectura ni distinguir una revisión de audio anterior. Las hipótesis posteriores no recuperan cuaderno, por lo que la posición se mantiene en 55.

La marca humana de cuaderno es 75,14–77,34 s y está completamente contenida tanto en 70–78 como en 72–80 s. El corte 80 s vuelve a reconocer parte del audio ya analizado; no acredita que el lector haya vuelto a pronunciar un. El diagnóstico identifica el mecanismo de decisión del seguidor, pero no aísla la causa acústica o interna por la que el ASR cambia cuaderno por jugaderno. No se atribuye el cambio al ruido ni a una nueva pronunciación del usuario.

## Comprobación y límite

Pasan dos pruebas que reproducen el mecanismo con un cuento mínimo y verifican que conservar cuaderno en la hipótesis mantiene el final. No se cambia seguir.py ni la variante de palabra aislada. La decisión sobre una corrección queda pendiente de revisión compartida. Una solución deberá distinguir revisiones de audio ya reconocido de relecturas reales; bloquear todos los retrocesos también bloquearía un comportamiento legítimo del lector.
