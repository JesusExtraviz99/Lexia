# Intentos parciales: «regres- re- regresar»

26/10/2026. El lector confirma pérdida de intentos en toma 3. La grafía del candidato es «regresar»; la secuencia comunicada es «regres- re- regresar». No hay tiempos humanos interiores ni referencia exhaustiva de intentos. Los guiones del texto bruto no son etiquetas de un clasificador propio.

## Diseño

Referencia fijada: resultados/literalidad/20261026_082404_701027_cola_vad_UTC. Se reutilizan el literal original con límite VAD, sus parámetros y arrays. No se cambia el VAD ni se añaden prompts del cuento o de la palabra objetivo. Modelo CrisperWhisper2.0 Small fijado, backend Transformers CPU float32, cuatro hilos, entorno aislado existente.

Se seleccionan toma 3 (desarrollo, intentos) y toma 2 (desarrollo, control de cuatro repeticiones). Tomas 5/6 reservadas: no se procesan ni se usan para ajustar. Para cada toma se reconoce de nuevo con una sola diferencia respecto a referencia:

1. hallucination_mitigation=False: desactivar reparación de repeticiones.
2. temperature_fallback=False: desactivar temperaturas alternativas.
3. early_eot_recovery=False: desactivar recuperación de cierre anticipado.

No se combinan cambios. Son seis inferencias; referencia previa reutilizada, no una nueva pasada pareada ni benchmark de velocidad. Igualdad de texto no demuestra si cada mecanismo se ejecutó o causó originalmente la omisión.

Diagnóstico adicional separado: extraer el último bloque acústico de toma 3, 52–70,32 s, según su salida nativa anterior. Se reconoce sin contexto textual previo con los ajustes originales. Cambian entrada, contexto y ruta corta/larga: no atribuir diferencias a una única causa. La marca automática de regresar 60,10–60,68 s es solo orientación para escuchar. El recorte no usa una marca humana ni corta precisamente el intento. Se conserva el límite final VAD y el original completo.

## Reproducibilidad y revisión

scripts/analizar_intentos_literal.py prepara manifiesto nuevo, huellas de fuentes/arrays/modelo, parámetros y fuente exacta; ejecuta siete propuestas con un modelo reutilizado, sin sobrescribir resultados. CPU, RAM, GPU global y bloques/palabras automáticos se conservan. Las marcas del recorte son relativas a su entrada; absolute_start permite relacionarlas con el original. No se validan como límites humanos.

```powershell
.\.venv\Scripts\python.exe -m scripts.analizar_intentos_literal preparar
# Usar la carpeta que devuelve, sin repetir el experimento ya ejecutado:
.\.tools\literal-env\Scripts\python.exe -u -m scripts.analizar_intentos_literal ejecutar RUTA_RESULTADOS
.\.venv\Scripts\python.exe -m scripts.analizar_intentos_literal resumir RUTA_RESULTADOS
```

Tanda actual: resultados/literalidad/20261026_084437_140574_intentos_UTC. Conservar todas las salidas, también las que no mejoren. Revisar por escucha cualquier recuperación de intento y posibles inserciones; no calcular precisión con el cuento, otro ASR o guiones. Ninguna variante se activa automáticamente ni se publica sin indicación del usuario.

## Resultado

Las seis ablaciones son textualmente idénticas a referencia. El recorte aislado tampoco recupera regres- re-. Conclusiones y límites en la carpeta del experimento; ninguna variante se adopta. Inferencia total 108,46 s, carga 6,05 s. Visor local 8782 para escucha compartida.
