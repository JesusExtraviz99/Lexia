# MLS test con los doce candidatos fijados

Estado: preparado localmente; la ejecución remota debe iniciarse y comprobarse.

Se evalúan los 2.385 audios de MLS español test, distintos de los 2.408 dev. Todos usan los mismos archivos, referencias, normalización, pesos y parámetros de su prueba dev. No se afinan configuraciones con test. Los informes originales se conservan.

Motores: XLSR, Parakeet, Faster-Whisper Small, Vosk Small español, Crisper Small; Moonshine Tiny/Small español, Granite TurboCTC, Qwen ASR 0.6B/1.7B, Canary v2 y Whisper large-v3-turbo. Crisper Small conserva la referencia anterior; Crisper medium/turbo/large nuevos siguen solo descargados, sin pruebas.

## Instalación y arranque

Desde PowerShell en la raíz del proyecto:

```powershell
scp .\.descartados\servidor\lexia_mls_test_todos.tar .\.descartados\servidor\lexia_mls_test_todos.tar.sha256 jextraviz@192.168.22.24:/opt/qaisc/home/jextraviz/
```

En SSH:

```bash
cd "$HOME"
sha256sum -c lexia_mls_test_todos.tar.sha256 && tar -xf lexia_mls_test_todos.tar -C "$HOME/lexia"
cd "$HOME/lexia/experimentos/test_todos_20261106"
nvidia-smi
bash scripts/ejecutar_test_todos.sh 0 1 2 3
```

Reservar previamente en «Uso de los servidores» los índices autorizados. Se admite una lista menor, por ejemplo `0 1`; los demás esperan turno. Una tarea propia por GPU; Vosk en CPU. El lote usa `nohup`, entrada cerrada y log, por lo que puede continuar al cerrar SSH/VPN o apagar el ordenador local después de comprobar su arranque. La persistencia depende de que el servidor y la sesión de cómputo sigan funcionando.

```bash
python3 scripts/estado_asr_externo.py resultados/asr_externo/mls_test_todos_01
tail -n 30 resultados/asr_externo/mls_test_todos_01.lanzador.log
```

Primero se verifican versiones y 2.385 archivos; puede mostrarse «Preparación» antes de haber inferencias. El PID inicial no basta: verificar log, cohorte y progreso. El envoltorio rechaza salida/log/PID previos para evitar duplicar un arranque.

## Entornos, pesos y resultados anteriores

El paquete se extrae en una carpeta nueva y reutiliza los ejecutables y pesos de:

- `$HOME/lexia`: cinco modelos iniciales y sus entornos.
- `$HOME/lexia/experimentos/ampliacion_20261106`: siete ASR nuevos y su entorno.
- `$HOME/datasets_mls_evaluacion/mls_es`: dataset ya instalado.

No instala dependencias, descarga modelos ni altera Python del sistema. Las dependencias deben coincidir exactamente con las registradas en dev. El protocolo guarda sus versiones, parámetros, revisiones/huellas y huellas de las fuentes delegadas; el despachador conjunto es nuevo y su propia huella aparecerá en las nuevas ejecuciones.

Si el test original `mls_test_completo_paralela_01` ya contiene un motor completo, se comprueban configuración, firma, selección, referencias, huellas y todos sus resultados antes de copiarlo al informe conjunto. Se marca **reutilizado**, con recursos de su ejecución original. Si sigue activo, se espera su finalización sin duplicarlo. Si no existe o quedó detenido e incompleto, el motor se ejecuta en la carpeta nueva. Una configuración incompatible provoca error explícito, no reutilización silenciosa. Los experimentos originales no se modifican.

## Interpretación y recuperación de resultados

Se conservan las mismas métricas y telemetría del evaluador anterior: WER/CER y errores, tiempos/RTF, recursos por proceso y sistema, muestras GPU, carga/calentamiento, entorno y procedencia. Los máximos de recursos son observados mediante muestreo, no picos garantizados. La ejecución concurrente y la reutilización impiden interpretar los tiempos como un benchmark aislado entre todos los motores; tampoco mide seguimiento en directo o rendimiento de tablet.

Al terminar, comprobar `Estado: completed`, 2.385/2.385 y cero fallos por motor. Conservar logs y JSON, incluidos fallos si los hubiera. Para descargar desde PowerShell, primero empaquetar en SSH:

```bash
cd "$HOME/lexia/experimentos/test_todos_20261106"
tar -czf "$HOME/mls_test_todos_01.tar.gz" -C resultados/asr_externo mls_test_todos_01
cd "$HOME"
sha256sum mls_test_todos_01.tar.gz > mls_test_todos_01.tar.gz.sha256
```

```powershell
scp jextraviz@192.168.22.24:/opt/qaisc/home/jextraviz/mls_test_todos_01.tar.gz jextraviz@192.168.22.24:/opt/qaisc/home/jextraviz/mls_test_todos_01.tar.gz.sha256 .\.descartados\servidor\resultados\
```

La auditoría local posterior comprobará resultados y métricas antes de seleccionar candidatos. La revisión previa encontró algunas referencias oficiales incompletas: conservar puntuaciones oficiales y revisión humana separadas. La independencia de los corpus respecto al entrenamiento de cada modelo requiere revisión documental de particiones; no se presume por llamarse test.
