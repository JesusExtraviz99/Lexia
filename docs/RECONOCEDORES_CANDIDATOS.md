# Candidatos ASR instalados · 28/10/2026

Entorno nuevo .tools/asr-candidatos-env, Python 3.12.15. No modifica .venv ni .tools/literal-env. Instalación inicial en CPU: PyTorch 2.14.1+cpu, Transformers 5.20.2, Vosk 0.3.45, librosa 1.0.0; todas las dependencias fijadas en requirements-asr-candidatos-lock.txt. Los backends/precisiones son parte de cada configuración y no se ocultan al comparar modelos.

| Clave | Reconocedor local | Configuración preparada | Fuente |
|---|---|---|---|
| xlsr | modelos/wav2vec2-xlsr-53-spanish | wav2vec2 XLSR-53 español, CTC greedy sin modelo de lenguaje externo; Transformers CPU float32, cuatro hilos Torch. | https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-spanish |
| vosk | modelos/vosk-model-small-es-0.42 | Vosk Small español 0.42 con su grafo de decodificación; API 0.3.45 en CPU. Hilos nativos no fijados por el helper. | https://alphacephei.com/vosk/models |
| parakeet | modelos/parakeet-tdt-0.6b-v3 | Parakeet TDT 0.6B v3, Transformers CPU float32, cuatro hilos Torch. | https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3 |

Whisper Small y CrisperWhisper Small se conservan en sus instalaciones previas y siguen siendo referencias. No se activa ninguno de los candidatos en el seguidor ni se modifican las reglas o el pipeline literal habitual.

## Procedencia y verificación

resultados/instalacion_asr/20261028_candidatos_cpu guarda revisiones completas de Hugging Face y huellas por archivo, metadatos del ZIP oficial Vosk, pruebas técnicas, recursos y resumen de instalación. XLSR revisión 96d7e9b4e4a78af515a3c6d3cee7c0826045d276; Parakeet 541d1f99c6b0c3cd0b11a95167540bb8edefd82b. El ZIP Vosk conserva versión y SHA256 local. Se coteja SHA256 de pesos con metadatos LFS publicados cuando están disponibles; Vosk se comprueba con CRC ZIP y huellas locales. No se ejecuta código Python del repositorio del modelo (trust_remote_code=False); se carga con implementaciones instaladas de Transformers y pesos locales. Los BIN de XLSR se cargan como pesos mediante weights_only=True.

Licencias declaradas: Apache-2.0 para XLSR/Vosk y CC-BY-4.0 para Parakeet. Metadatos y avisos del proveedor se conservan. Pesos, cachés y entornos están excluidos de Git; no subirlos como resultados del proyecto.

XLSR se configura explícitamente con Wav2Vec2FeatureExtractor, Wav2Vec2CTCTokenizer y Wav2Vec2Processor. El repositorio declara un procesador con modelo de lenguaje, pero la variante evaluable aquí es CTC directa, también documentada en su ficha. No se instala ni utiliza pyctcdecode/KenLM; esta diferencia debe constar al presentar resultados. No atribuir el rendimiento de esta variante a todas las posibles decodificaciones de XLSR.

## Pruebas técnicas completadas

Cada modelo se carga por separado y ejecuta un segundo de ceros a 16 kHz generado en memoria. Vosk construye el reconocedor y devuelve JSON; XLSR ejecuta forward CTC y decodificación; Parakeet ejecuta generate y decodifica sequences. Los tres terminan correctamente. No se ha activado micrófono, enviado audio o usado grabaciones/datasets. Es una prueba de funcionamiento; no mide precisión, conservación de intentos, WER, rendimiento de tablet ni latencia del producto. Los recursos registrados incluyen carga/importaciones, sobre una señal sintética, con trabajo de datasets posiblemente concurrente: no son un benchmark comparativo.

Para repetir una prueba técnica (solo señal sintética; escribe el resultado de esa clave):

```powershell
.\.tools\asr-candidatos-env\Scripts\python.exe -u -m scripts.preparar_asr_candidatos prueba xlsr --salida resultados/instalacion_asr/20261028_candidatos_cpu
```

Sustituir xlsr por vosk o parakeet. Las comparaciones con FLEURS/MLS y lecturas propias todavía necesitan fijar muestra, partición, referencias, normalización y ajustes. El propio proveedor de Parakeet señala limitaciones para transcripción palabra por palabra y frases incompletas; la carga correcta no valida ese uso.

Para recrear las dependencias en otro entorno aislado con uv, instalar requirements-asr-candidatos-lock.txt usando --torch-backend cpu. Los pesos de la comparación deben mantener las revisiones registradas, no sustituirse sin registrar el cambio por la versión más reciente.
