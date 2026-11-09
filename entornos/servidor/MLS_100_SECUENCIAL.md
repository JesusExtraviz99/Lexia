# MLS dev · 100 audios secuenciales sin Crisper

Preparado el 06/11/2026. Se conservan configuración, pesos, semilla 42 y evaluador de MLS dev completo. Los primeros 100 IDs de la selección barajada son comunes a los cuatro motores: 1493.21 s (24.89 min). No son datos nuevos ni una evaluación del seguidor: se mide el ASR que puede alimentarlo. Test no se utiliza.

Orden: XLSR, Parakeet, Faster-Whisper y Vosk. Una única tarea propia activa, incluido Vosk en CPU. GPU física 0 por la instrucción propuesta (se admite 1 explícitamente); ninguna otra se selecciona. La etiqueta aislada significa sin otros motores de esta cohorte, no servidor exclusivo: otros usuarios pueden compartir CPU/RAM/disco. Se mantiene la telemetría original y sus límites de muestreo. Una pasada por motor, sin prometer variabilidad entre repeticiones.

Antes de iniciar, reservar GPU en el calendario Uso de los servidores y comprobar nvidia-smi. Reservar inicialmente media hora con margen; es una estimación y se actualizará si el lote lo necesita. No reservar GPU 1 si solo se usa 0.

## Instalar la actualización (SSH)

```bash
cd "$HOME"
sha256sum -c lexia_mls_100_secuencial.tar.sha256 && tar -xf lexia_mls_100_secuencial.tar -C "$HOME/lexia"
cd "$HOME/lexia"
nvidia-smi
bash scripts/ejecutar_mls_dev_100_secuencial.sh 0
```

No ejecutar el lanzador de dev completo otra vez. El nuevo envoltorio nohup crea una carpeta nueva y rechaza salida/log/PID previos. No descarga pesos, modifica audios ni borra resultados. Sigue ejecutándose al cerrar SSH en condiciones normales.

## Consultar

```bash
cd "$HOME/lexia"
python3 scripts/estado_asr_externo.py resultados/asr_externo/mls_dev_100_secuencial_sin_crisper_01
tail -n 15 resultados/asr_externo/mls_dev_100_secuencial_sin_crisper_01.lanzador.log
```

Los motores no iniciados figuran en pendientes, sin fila de progreso todavía. Al final deben aparecer cuatro motores, 100/100, cero fallos y completed. Fuentes actualizadas comprobadas mediante 18 pruebas simuladas; no equivalen a ejecución real remota.
