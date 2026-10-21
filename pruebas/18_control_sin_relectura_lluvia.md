# Control sin relectura con lluvia

21/10/2026. WAV datos/audio/lectura_20261021_100814_321948.wav, 40 s. Lluvia comunicada por el usuario; sin comparación emparejada para medir su efecto. Consigna: cuento completo una vez y después silencio. El usuario confirma una sola lectura; sin validación lexical palabra por palabra ni marcas temporales nuevas.

El usuario comparte resultados/comparaciones/20261021_100926_258927 (ventanas 4/8 s, tres rondas, bloques 2 s). Repetir la comparación de seguidores, sin inferencias nuevas:

```powershell
.\.venv\Scripts\python.exe -m scripts.comparar_relectura_lejana resultados/comparaciones/20261021_100926_258927 --control-sin-relectura
```

Ejecución del asistente: resultados/controles_sin_relectura/20261021_101354_783663. Los tres seguidores coinciden en todas las posiciones, no hay movimientos negativos ni recuperaciones exactas y todos conservan 56 después de alcanzarlo. El usuario comparte resultados/controles_sin_relectura/20261021_101537_824815. Coinciden íntegramente los seis registros con los del asistente. Revisión compartida completada. Tres rondas de un solo audio no estiman una tasa general de falsos positivos. No hay marcas humanas nuevas ni cambios de reglas. No se activa ni publica automáticamente.
