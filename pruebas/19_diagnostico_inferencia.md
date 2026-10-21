# Diagnóstico de los reintentos ASR

21/10/2026. Nuevas inferencias instrumentadas, sin modificar configuración habitual ni seguidor. WAV lectura_20261021_100814_321948.wav.

Para repetir el contraste central (seis llamadas sobre el mismo corte, tres rondas):

```powershell
.\.venv\Scripts\python.exe -u -m scripts.diagnosticar_inferencia resultados/comparaciones/20261021_100926_258927 --solo-corte 22
```

Para el diagnóstico ampliado con cortes vecinos, omitir --solo-corte 22. La opción --sin-fallback limita la temperatura a 0, solo como ablación experimental; no se recomienda como cambio habitual. No descargar modelos: usa el modelo local. La salida muestra tiempos por etapa y las temperaturas de cada llamada de generación; el JSON conserva textos de intentos descartados y sus métricas. La primera llamada puede incluir calentamiento; no es un benchmark emparejado con tiempos antiguos. Las temperaturas no nulas pueden variar el texto/tiempo.

Evidencia del asistente: resultados/diagnostico_inferencia/20261021_101852_059105/diagnostico.md. Ventana 8 s/corte 22 genera inicialmente repetición excesiva (razón de compresión >2,4) y reintenta a 0,2 y 0,4; cortes vecinos y ventana 4 s usan 0. La ablación resultados/diagnostico_inferencia/20261021_102019_524726 reduce tiempo pero conserva repetición/texto ajeno al cuento. No se atribuye la dificultad a la lluvia. Pendiente de revisión compartida.
