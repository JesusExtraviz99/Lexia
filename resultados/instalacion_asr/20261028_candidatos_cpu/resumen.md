# Instalación de candidatos ASR · 28/10/2026

Instalados en entorno aislado .tools/asr-candidatos-env. Dependencias fijadas en requirements-asr-candidatos-lock.txt. No se modifica Whisper/CrisperWhisper ni se ejecuta ASR sobre audios propios/datasets.

| Candidato | Revisión | Prueba técnica CPU |
|---|---|---|
| xlsr | 96d7e9b4e4a78af515a3c6d3cee7c0826045d276 | correcta |
| vosk | Small español 0.42, ZIP oficial | correcta |
| parakeet | 541d1f99c6b0c3cd0b11a95167540bb8edefd82b | correcta |

Prueba con un segundo sintético de ceros mono 16 kHz. Verifica carga/ejecución/decodificación, no calidad o rendimiento móvil. XLSR = CTC greedy sin LM externo; Vosk = grafo incluido; Parakeet = TDT Transformers. Recursos por prueba en JSON, no benchmark comparativo.

Pesos y versiones fijados, fuentes exactas conservadas. Detalles y comandos: docs/RECONOCEDORES_CANDIDATOS.md. Sin publicación automática ni modelo adoptado.
