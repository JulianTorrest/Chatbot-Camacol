# Reasoning System vs “reentrenar agente” (RAG) — relación, roles e insumos/salidas

Este documento explica:

- qué hace `reasoning_system.py`
- qué significa “reentrenar” en este proyecto (en la práctica: **re-indexar / actualizar el RAG**)
- si están relacionados o no
- cuál es el **insumo** y **salida** de cada módulo en el flujo principal (`app.py` / `bot_telegram.py`).

---

## 1) Definición rápida (qué es cada uno)

### 1.1 `ReasoningSystem` (reasoning_system.py)

- **Qué hace**: es un **módulo de razonamiento/reglas de clarificación**.
- **Función principal**: analiza la pregunta del usuario y decide si está:
  - completa
  - incompleta
  - ambigua
  - necesita clarificación

- **Salida principal**: un `ReasoningResult` con:
  - `question_type`
  - `missing_elements`
  - `counter_questions`
  - `reasoning_comments`
  - `suggested_clarifications`

- **Rol en el sistema**:
  - *“Gatekeeper”* (puerta de entrada) antes de ejecutar LIVO/RAG.
  - Evita consultas mal definidas (por ejemplo, en LIVO) y pide precisión (cuenta, ubicación, período, métrica).

- **Insumos**:
  - texto del usuario (`question`)
  - `user_id`
  - historial (opcional) `conversation_history`
  - (opcional) perfil del usuario vía `user_profile_manager`.

- **Nota técnica importante**:
  - En `reasoning_system.py`, `analyze_question` está definido como:
    - `analyze_question(self, question: str, user_id: str, conversation_history: List[str] = None)`
  - O sea: el reasoning requiere `user_id` (en Streamlit/Telegram se usa).

---

### 1.2 “Reentrenar el agente” en este repo (RAGSystem / inicializar_rag.py)

En este proyecto, “reentrenar” no es fine-tuning de un LLM. Es:

- **reconstruir o actualizar el índice vectorial** de documentos (RAG)
- generar/actualizar el cache (`rag_cache/vectorstore.pkl`) y manifiestos

**Componentes**:

- `rag_system.py`:
  - clase `RAGSystem`
  - métodos relevantes:
    - `inicializar(force_reload: bool=False)`
    - `buscar(query, k)`
    - `buscar_con_analisis(query, k)`
    - `listar_documentos()`

- `inicializar_rag.py`:
  - script para ejecutar “una vez” o cuando cambian documentos.
  - calcula hashes de archivos y decide si hay cambios.
  - llama `rag_system.inicializar(force_reload=...)`.

- **Salida principal**:
  - un vector store (FAISS) + metadata + manifiesto.

- **Insumos**:
  - documentos en carpeta `RAG/` (PDF, DOCX, XLSX, CSV, PPTX)
  - (opcional) URLs listadas en un archivo (porque `RAGSystem` tiene lógica de descarga y procesamiento de URLs)

---

## 2) ¿Están relacionados ReasoningSystem y RAG “reentrenamiento”?

### Relación real (en runtime)

- `ReasoningSystem` **no “entrena”** el RAG.
- `ReasoningSystem` **no modifica** el índice.
- El RAG se (re)inicializa por:
  - `inicializar_rag.py` (offline / manual)
  - o desde la UI de `app.py` con el botón **“🔄 Recargar RAG”** que llama `rag_system.inicializar(force_reload=True)`.

### Relación funcional

- Sí están relacionados en el sentido de **orquestación del flujo**:
  - `ReasoningSystem` decide si la pregunta está lista o requiere clarificación.
  - cuando está lista, el flujo continúa hacia LIVO o RAG.

Pero a nivel de “reentrenar”:

- `ReasoningSystem` **no es el insumo** del reentrenamiento.
- `ReasoningSystem` **no produce salida** usada para construir embeddings.

---

## 3) ¿Dónde entran en el proceso principal?

### 3.1 En Streamlit (`app.py`)

1) Se inicializa `ReasoningSystem()` en `st.session_state`.
2) En cada prompt (si no es “pregunta simple”), se ejecuta:

- `analysis_result = analyze_and_respond(question, user_id, reasoning_system, conversation_history)`

3) Si `needs_clarification=True`:

- se responde al usuario con las contrapreguntas
- **se corta el flujo** (`st.stop()`)

4) Si no necesita clarificación:

- si es “tipo_pregunta == datos” se intenta LIVO SQL
- si falla LIVO, fallback a RAG
- si no es datos, se usa RAG para el resto

Adicionalmente:

- existe un panel “Gestión RAG” que permite:
  - ver documentos (`listar_documentos()`)
  - recargar (`inicializar(force_reload=True)`) — esto es “reentrenar” en el sentido operativo

---

### 3.2 En Telegram (`bot_telegram.py`)

- Se inicializa `ReasoningSystem()` global.
- Se inicializa `RAGSystem()` global y se llama `inicializar()` al inicio.

En el procesamiento de mensajes (handlers), el bot típicamente:

- usa reasoning para clarificar
- luego rutea hacia LIVO / Coyuntura SQL / RAG / LLM

---

## 4) Matriz: insumo/salida por módulo

### 4.1 ReasoningSystem

- **Insumo**:
  - texto (pregunta)
  - historial (opcional)
  - user_id (perfil)
- **Salida**:
  - `ReasoningResult`
  - texto de clarificación (si aplica)
- **Consumidor principal**:
  - `app.py` (antes de LIVO/RAG)
  - `bot_telegram.py` (antes de LIVO/RAG)

### 4.2 RAGSystem (re-index / “reentrenar”)

- **Insumo**:
  - carpeta `RAG/` (documentos)
  - (opcional) URLs para descargar docs
- **Salida**:
  - `rag_cache/vectorstore.pkl`
  - `metadata` y `manifest`
  - consultas semánticas (`buscar`) que retornan top-k fragmentos
- **Consumidor principal**:
  - `app.py` para responder preguntas no resueltas por LIVO
  - `bot_telegram.py` como fallback o fuente principal documental

---

## 5) Diagrama PlantUML

Ver `REASONING_RAG_PLANTUML.puml`.
