# 🤖 Agente de Predicción de Abandono de Empleados
### Agentic AI – Universidad Central del Ecuador 2026

Un agente de inteligencia artificial autónomo que predice el riesgo de abandono laboral usando Machine Learning, genera recomendaciones automáticas con IA generativa y mantiene un historial de decisiones persistente.

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Arquitectura](#arquitectura)
- [Requisitos Previos](#requisitos-previos)
- [Instalación en Windows](#instalación-en-windows)
- [Instalación en macOS](#instalación-en-macos)
- [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
- [Ejecutar el Proyecto](#ejecutar-el-proyecto)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Dataset](#dataset)
- [Equipo](#equipo)

---

## Descripción

El agente implementa los 5 componentes de un sistema Agentic AI:

| Componente | Implementación |
|---|---|
| **Percepción** | Lee y limpia `empleados.csv` (11 features validadas) |
| **Razonamiento** | Modelo ML: Logistic Regression / Random Forest / XGBoost |
| **Acción** | Recomendaciones via API de Claude (Anthropic) + reporte CSV automático para RRHH |
| **Memoria** | Historial persistente en SQLite (`database.db`) |
| **Interfaz** | Dashboard web interactivo con Streamlit |

---

## Arquitectura

```
project/
├── app.py                  # Interfaz Streamlit
├── agent.py                # Lógica central del agente
├── database.py             # Gestión SQLite
├── data_cleaning.py        # Limpieza y preprocesamiento
├── models/
│   └── model.pkl           # Modelo ML entrenado
├── database/
│   └── database.db         # Base de datos SQLite
├── reports/
│   └── reporte_riesgo_empleados.csv
├── data/
│   └── empleados.csv       # Dataset sintético (10,000 registros)
└── train_model.ipynb       # Notebook de entrenamiento
```

---

## Requisitos Previos

- Python **3.10** o superior
- `pip` actualizado
- Clave de API de **Anthropic (Claude)** — para las recomendaciones automáticas. Obtenerla en [console.anthropic.com](https://console.anthropic.com)
- Git (opcional, para clonar el repositorio)

---

## Instalación en Windows

### 1. Verificar Python

Abre **PowerShell** o **CMD** y ejecuta:

```powershell
python --version
```

Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/). Durante la instalación, **marca la casilla "Add Python to PATH"**.

### 2. Clonar el repositorio

```powershell
git clone https://github.com/tu-usuario/agentic-ai-attrition.git
cd agentic-ai-attrition
```

> Si no usas Git, descarga el ZIP desde GitHub y extráelo.

### 3. Crear el entorno virtual

```powershell
python -m venv venv
```

### 4. Activar el entorno virtual

```powershell
venv\Scripts\activate
```

Deberías ver `(venv)` al inicio de la línea de tu terminal.

### 5. Actualizar pip e instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Entrenar el modelo (primera vez)

```powershell
jupyter notebook train_model.ipynb
```

O si prefieres ejecutarlo directamente:

```powershell
jupyter nbconvert --to notebook --execute train_model.ipynb
```

Esto generará el archivo `models/model.pkl`.

---

## Instalación en macOS

### 1. Verificar Python

Abre **Terminal** y ejecuta:

```bash
python3 --version
```

Si no tienes Python 3.10+, instálalo con [Homebrew](https://brew.sh/):

```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.11
```

### 2. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/agentic-ai-attrition.git
cd agentic-ai-attrition
```

### 3. Crear el entorno virtual

```bash
python3 -m venv venv
```

### 4. Activar el entorno virtual

```bash
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de la línea de tu terminal.

### 5. Actualizar pip e instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Entrenar el modelo (primera vez)

```bash
jupyter notebook train_model.ipynb
```

Esto generará el archivo `models/model.pkl`.

---

## Configuración de Variables de Entorno

El agente necesita una clave de API para generar recomendaciones con IA generativa.

### Windows (PowerShell)

```powershell
copy .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

Luego abre el archivo `.env` con cualquier editor de texto y agrega tu clave:

```env
# Usa UNA de las dos opciones según la API que tengas

# Opción A – OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Opción B – Google Gemini
GEMINI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> **Nota:** Si no tienes ninguna clave de API, el agente igual funcionará para predicción y clasificación de riesgo, pero las recomendaciones automáticas estarán deshabilitadas.

---

## Ejecutar el Proyecto

Con el entorno virtual activado y las variables configuradas:

### Windows

```powershell
streamlit run app.py
```

### macOS

```bash
streamlit run app.py
```

El navegador se abrirá automáticamente en `http://localhost:8501`.

Si no se abre solo, cópialo manualmente en tu navegador.

---

## Uso de la Aplicación

1. **Cargar datos** — Sube el archivo `empleados.csv` desde el panel lateral
2. **Ejecutar predicción** — Haz clic en "Analizar empleados"
3. **Ver resultados** — El dashboard muestra el riesgo (Bajo / Medio / Alto) y la recomendación para cada empleado
4. **Consultar historial** — La pestaña "Historial" muestra todas las evaluaciones anteriores guardadas en SQLite
5. **Descargar reporte** — El reporte CSV con empleados de riesgo alto se genera automáticamente en `reports/`

---

## Dataset

El proyecto incluye un dataset sintético de **10,000 registros** con las siguientes variables de entrada al modelo:

| Feature | Tipo | Descripción |
|---|---|---|
| `edad` | Numérica | Edad del empleado |
| `salario` | Numérica | Salario mensual |
| `experiencia` | Numérica | Años de experiencia total |
| `antiguedad_empresa` | Numérica | Años en la empresa actual |
| `departamento` | Categórica | Área de trabajo |
| `tipo_contrato` | Categórica | Modalidad contractual |
| `horas_trabajo` | Numérica | Horas semanales |
| `satisfaccion_laboral` | Ordinal (1-5) | Nivel de satisfacción |
| `work_life_balance` | Ordinal (1-5) | Balance vida-trabajo |
| `promociones` | Numérica | Número de promociones |
| `distancia_trabajo` | Numérica | Km al trabajo |

**Variable target:** `renuncia` — binaria (0 = no renuncia / 1 = sí renuncia)

---

## Dependencias

Listado completo del archivo `requirements.txt` con versiones exactas:

### Interfaz y Visualización

| Paquete | Versión | Uso |
|---|---|---|
| `streamlit` | 1.56.0 | Dashboard web interactivo |
| `altair` | 6.0.0 | Gráficos declarativos en Streamlit |
| `matplotlib` | 3.10.8 | Gráficas estáticas |
| `seaborn` | 0.13.2 | Visualización estadística |
| `pydeck` | 0.9.1 | Mapas y visualizaciones geoespaciales |
| `pillow` | 12.2.0 | Procesamiento de imágenes |

### Machine Learning y Datos

| Paquete | Versión | Uso |
|---|---|---|
| `scikit-learn` | 1.8.0 | Logistic Regression, Random Forest, preprocesamiento |
| `pandas` | 3.0.2 | Manipulación y análisis de datos |
| `numpy` | 2.4.4 | Operaciones numéricas |
| `scipy` | 1.17.1 | Funciones científicas y estadísticas |
| `joblib` | 1.5.3 | Serialización del modelo `.pkl` |
| `pyarrow` | 23.0.1 | Lectura eficiente de datos tabulares |
| `narwhals` | 2.19.0 | Compatibilidad entre dataframes |

### IA Generativa y HTTP

| Paquete | Versión | Uso |
|---|---|---|
| `anthropic` | 0.94.0 | Cliente para API de Claude (opcional) |
| `httpx` | 0.28.1 | Cliente HTTP para llamadas a APIs externas |
| `httpcore` | 1.0.9 | Transporte HTTP de bajo nivel |
| `requests` | 2.33.1 | Solicitudes HTTP generales |
| `tenacity` | 9.1.4 | Reintentos automáticos en llamadas a API |

### Configuración y Utilidades

| Paquete | Versión | Uso |
|---|---|---|
| `python-dotenv` | 1.2.2 | Carga de variables de entorno desde `.env` |
| `pydantic` | 2.12.5 | Validación de datos y esquemas |
| `python-dateutil` | 2.9.0 | Manejo avanzado de fechas |
| `toml` | 0.10.2 | Lectura de archivos de configuración |
| `click` | 8.3.2 | Interfaz de línea de comandos |
| `GitPython` | 3.1.46 | Interacción con repositorios Git |
| `watchdog` | 6.0.0 | Hot-reload de Streamlit en desarrollo |

### Tipado y Validación

| Paquete | Versión | Uso |
|---|---|---|
| `typing_extensions` | 4.15.0 | Tipos adicionales para Python 3.10+ |
| `annotated-types` | 0.7.0 | Soporte de tipos anotados |
| `pydantic_core` | 2.41.5 | Motor de validación de Pydantic |
| `jsonschema` | 4.26.0 | Validación de esquemas JSON |

> Para instalar todas las dependencias de una vez: `pip install -r requirements.txt`

---

## Equipo

| Rol | Responsabilidad |
|---|---|
| Data Engineer | Dataset CSV, limpieza, validación |
| ML Engineer | Entrenamiento de modelos, métricas, selección de features |
| Agent Engineer | Lógica agent.py, clasificación, SQLite, reporte CSV |
| Interface Engineer | app.py Streamlit, visualización, historial |
| Documentation Engineer | Documento técnico PDF, PPT, README |

---

## Licencia

Proyecto académico – Universidad Central del Ecuador, Facultad de Ingeniería en Sistemas e Informática – Abril 2026.