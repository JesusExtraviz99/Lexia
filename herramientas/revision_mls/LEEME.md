# Revisión auditiva MLS dev

Ejecutar desde la raíz: `.\.venv\Scripts\python.exe -u -m scripts.revisar_mls_web --puerto 8850` y abrir http://127.0.0.1:8850/ en Chrome. Servidor solo local.

Nueve casos únicos: tres prioritarios (repetición extensa Crisper y posibles referencias incompletas), tres con marcas fuera de rango y unión de los tres mayores WER de cada motor. Una selección de diagnóstico, no muestra estadística representativa.

Escuchar primero sin hipótesis; después mostrarlas y comparar. Indicar valoración de referencia, motores con errores confirmados, nota y transcripción opcional del fragmento. Confirmar escucha/caso revisado solo tras hacerlo. Guardar antes de cambiar de caso o cerrar; se puede continuar más tarde. Las dudas pueden marcarse explícitamente. No se exige transcribir clips enteros.

Originales FLAC cotejados por SHA256. Copias WAV PCM16 sin filtros/recortes en .descartados/revision_mls/audio; se comparan muestras y frecuencia con el FLAC. No son reconocimientos nuevos. Hipótesis y tiempos proceden del lote guardado. Anotaciones en resultados/asr_externo/mls_dev_completo_paralela_01/revision_completa/escucha_humana, con respaldos locales de versiones anteriores. No modifica las referencias ni recalcula métricas automáticamente.

Ocho pruebas correctas de validación, guardado/reanudación y revisión previa de lectores. Visor comprobado en Chrome sin simular escucha o completar anotaciones humanas.
