# MLS test completo · cinco candidatos fijados

06/11/2026: 2.385 audios nuevos de test oficial, 36.013,14 s (~10 h) por motor. Se conserva el evaluador, adaptador, pesos, versiones y parámetros del lote dev. Baseline documentado en MLS_TEST_PROTOCOLO.json. No se modifican referencias según revisiones de casos de dev. Test mide esta configuración fijada; futuros cambios o nuevos modelos necesitan su propio desarrollo, y no se ajustan para ganar esta partición.

Crisper se incluye: su exclusión se limitó al experimento secuencial de 100. Con GPU 0 1 2 3 disponibles: XLSR→0, Parakeet→1, Faster-Whisper→2, Crisper→3, Vosk→CPU. Una tarea propia por GPU autorizada; si alguna está ocupada espera o redistribuye dentro de la lista explícita. No usa otras tarjetas ni cambia a CPU silenciosamente. Resultados concurrentes, no rendimiento aislado.

## Antes de iniciar

Reservar en Uso de los servidores, título Deeplearning NOMBRE (GPU: 0, 1, 2, 3), con intervalo previsto y margen. Según dev, estimar hasta unas tres horas para el conjunto, sin garantía; actualizar reserva según avance y liberar tarjetas terminadas. nvidia-smi no sustituye reserva.

## SSH

```bash
cd "$HOME"
sha256sum -c lexia_mls_test_completo.tar.sha256 && tar -xf lexia_mls_test_completo.tar -C "$HOME/lexia"
cd "$HOME/lexia"
nvidia-smi
bash scripts/ejecutar_mls_test_completo.sh 0 1 2 3
```

Envoltorio nohup desacoplado de SSH; salida nueva mls_test_completo_paralela_01, nunca sobrescribe dev ni el lote secuencial. Sin instalaciones/descargas. Paquete de coordinador, envoltorio, progreso, guía y protocolo. No reextraer paquetes previos sobre esta versión. Checksum con LF.

```bash
cd "$HOME/lexia"
python3 scripts/estado_asr_externo.py resultados/asr_externo/mls_test_completo_paralela_01
tail -n 20 resultados/asr_externo/mls_test_completo_paralela_01.lanzador.log
```

Cinco motores deben completar 2385/2385 con cero fallos. Mismas métricas y telemetría del lote dev: WER/CER/alineamientos, tiempos con carga/calentamiento aparte, proceso/sistema, RAM/VRAM y GPU/potencia/muestras. Tras recuperar se auditarán IDs/huellas y métricas; no inferir precisión porque termine sin errores. No es prueba de literalidad infantil ni de tablet.

Validación local: 20 pruebas simuladas y sintaxis Bash correctas; se verifica la propagación de test y su confirmación a los cinco procesos, además de compatibilidad con dev y modo secuencial. No es ejecución real de test.
