# Guía de ejecución local (Windows + PowerShell)

Esta guía es para una persona que **descargó/descomprimió el proyecto por primera vez**, no tiene Python instalado y quiere ejecutar:

- **Streamlit local** (`app.py`)
- **Bot de Telegram local** (`bot_telegram.py`)

> Importante:
> - Todos los comandos están pensados para **PowerShell**.
> - Ejecuta PowerShell **como usuario normal** (no es necesario administrador salvo que winget lo pida).
> - Reemplaza los valores de tokens/keys por los reales.

---

## 0) Abrir PowerShell en la carpeta del proyecto

Ubica la carpeta del proyecto (la que contiene `requirements.txt`, `app.py`, `bot_telegram.py`).

Puedes abrir PowerShell desde el Explorador de archivos:

- Click derecho dentro de la carpeta -> **“Abrir en Terminal”** (o “Open in Terminal”).

---

## 1) Instalar Python con winget (si NO está instalado)

### 1.1 Verifica si ya existe Python

```powershell
python --version
py --version
```

Si alguno funciona, puedes saltar a la sección **2)**.

### 1.2 Instala Python (recomendado 3.11)

```powershell
winget install -e --id Python.Python.3.11
```

Cierra y vuelve a abrir PowerShell, y valida:

```powershell
python --version
pip --version
```

---

## 2) (Opcional pero recomendado) Instalar Git y Git LFS

### 2.1 Verifica Git

```powershell
git --version
```

Si no está:

```powershell
winget install -e --id Git.Git
```

Cierra y vuelve a abrir PowerShell y valida:

```powershell
git --version
```

### 2.2 Git LFS (solo si el repo usa archivos grandes en LFS)

```powershell
git lfs version
```

Si no existe:

```powershell
winget install -e --id GitHub.GitLFS
```

Luego (si el proyecto usa LFS):

```powershell
git lfs install
git lfs pull
```

---

## 3) Crear y activar el entorno virtual (venv)

En la raíz del proyecto:

```powershell
python -m venv .venv
```

Activar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación (ExecutionPolicy), ejecuta esto **solo para esta sesión**:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Verás el prefijo `(.venv)` al inicio de la línea.

---

## 4) Instalar dependencias

Con el entorno activado:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5) Configurar credenciales / variables de entorno

Este proyecto puede requerir variables para:

- Streamlit (por ejemplo `GOOGLE_API_KEY` en `.streamlit/secrets.toml`)
- Telegram (por ejemplo `TELEGRAM_TOKEN` en `.env`)

### 5.1 Streamlit: crear `.streamlit/secrets.toml`

En la raíz del proyecto, crea la carpeta y el archivo:

```powershell
New-Item -ItemType Directory -Force .streamlit | Out-Null
notepad .streamlit\secrets.toml
```

Ejemplo mínimo:

```toml
GOOGLE_API_KEY = "TU_API_KEY_AQUI"
```

### 5.2 Telegram: crear `.env`

En la raíz del proyecto:

```powershell
notepad .env
```

Ejemplo mínimo:

```env
TELEGRAM_TOKEN=TU_TOKEN_DE_BOTFATHER
```

> Si tu proyecto usa más variables (OpenAI, Anthropic, etc.), agrégalas también en `.env`.

---

## 6) Ejecutar Streamlit local

Con el entorno activado:

```powershell
streamlit run app.py
```

Abre en el navegador:

- `http://localhost:8501`

Para detener: `Ctrl + C`.

---

## 7) Ejecutar el bot de Telegram local

En otra terminal (o deteniendo Streamlit), con el entorno activado:

```powershell
python bot_telegram.py
```

Para detener: `Ctrl + C`.

---

## 8) Solución rápida de problemas

### 8.1 “`streamlit` no se reconoce”

Asegúrate de:

- Estar con el entorno activado `(.venv)`
- Haber instalado dependencias

Luego prueba:

```powershell
pip show streamlit
```

### 8.2 Error de token de Telegram

Si aparece que no encontró `TELEGRAM_TOKEN`:

- Verifica que el archivo `.env` exista en la **raíz del proyecto**
- Verifica que tenga la línea `TELEGRAM_TOKEN=...`

### 8.3 Error de API Key (Streamlit / Gemini)

- Verifica que exista `.streamlit/secrets.toml`
- Verifica que tenga `GOOGLE_API_KEY = "..."`

---

## 9) Comandos “resumen” (lista corta)

```powershell
# Instalar Python
winget install -e --id Python.Python.3.11

# (Opcional) Git
winget install -e --id Git.Git

# (Opcional) Git LFS
winget install -e --id GitHub.GitLFS

# En la carpeta del proyecto
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Streamlit
streamlit run app.py

# Telegram
python bot_telegram.py
```
