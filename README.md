# Bot Wizard — Finalización Wizard

> Herramienta de automatización RPA para la gestión de folios de **Atención a Autoridades** en los sistemas internos BBVA.

---

## 📋 Descripción

**Bot Wizard** es una aplicación de escritorio construida con Python y CustomTkinter que permite ejecutar procesos de automatización web (RPA) sobre los sistemas internos de la organización, específicamente:

| Acción | Sistema | Descripción |
|---|---|---|
| **Iniciar Sesión** | Google Drive | Guarda la sesión de Google de forma persistente para el perfil del bot |
| **Cierre Folio Wizard** | Wizard Autom Express | Finaliza tareas pendientes en el sistema Wizard a partir del archivo `Oficios.xlsx` |
| **Adjuntar Informe SUGO** | Intranet / BOIXP | Sube el informe de cierre de operaciones de asignación jurídica al sistema SUGO |

---

## 🗂️ Estructura del proyecto

```
wizard-finalizacion-folios/
├── main.py                        # Punto de entrada de la aplicación
├── Oficios.xlsx                   # Archivo de entrada con los folios a procesar
├── requirements.txt
├── README.md
├── .gitignore
│
├── dist/                          # ⚠️ Generado en runtime — NO se sube al repo
│   ├── perfil_google_drive/       # Sesión persistente de Chrome (Google Drive)
│   ├── Documentos/                # Informes PDF a subir al sistema SUGO
│   └── resultados_procesados.csv  # Registro de resultados por folio
│
└── app/
    ├── assets/                    # Imágenes e ícónos de la UI
    │   ├── bbva-blue.png
    │   ├── bbva-white.png
    │   ├── on-off.png
    │   ├── security-token-white.png
    │   └── trash-white.png
    │
    ├── config/
    │   └── settings.py            # Rutas, URLs, colores y constantes globales
    │
    ├── core/
    │   └── bots.py                # Lógica RPA: autenticación, orchestrator, Playwright
    │
    └── ui/
        ├── main_window.py         # Ventana principal e integración UI ↔ bots
        ├── panel_controls.py      # Panel izquierdo: botones + switch modo oculto
        ├── panel_logs.py          # Panel derecho: terminal de logs en tiempo real
        └── dialog_login.py        # Diálogo modal de credenciales (Intranet SUGO)
```

---

## ⚙️ Requisitos

- **Python** 3.10 o superior
- **Google Chrome** instalado (el bot usa el canal `chrome`)
- Acceso a los sistemas internos de la organización

---

## 🚀 Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd wizard-finalizacion-folios

# 2. Crear y activar entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Instalar dependencias Python
pip install -r requirements.txt

# 4. Instalar el navegador de Playwright
playwright install chromium
```

---

## ▶️ Uso

```bash
python3 main.py
```

### Flujo de trabajo recomendado

1. **Preparar** el archivo `Oficios.xlsx` en la raíz del proyecto con las columnas requeridas:
   `Folio Sugo`, `Folio Wizard`, `Tipo Respuesta`, `Selfservice`, `Dictamen Wizard`, `Informe`

2. **Seleccionar las carpetas de entrada** con los botones **Examinar** de la aplicación:
   - **Informes:** contiene los archivos de informe; el nombre debe incluir el folio SUGO. Se busca directamente en esta carpeta.
   - **Insumos:** contiene archivos cuyo nombre incluye el folio SUGO o subcarpetas con el folio en su nombre. Se buscan archivos recursivamente y se incluye todo el contenido de las subcarpetas coincidentes, sin duplicados.

   Ambas selecciones se guardan por separado y se restauran al abrir la aplicación. Si no hay una selección válida, se usan `informes/` e `insumos/` junto al programa cuando existan. Para **Adjuntar Informe / Insumos**, ambas rutas deben ser carpetas existentes; el informe es obligatorio para cada folio que requiere carga.

3. En la aplicación:
   - Presionar **1. Iniciar Sesión** para autenticar el perfil de Google (solo la primera vez)
   - Presionar **2. Cierre Folio Wizard** para procesar los folios en el sistema Wizard
   - Presionar **3. Adjuntar Informe SUGO** para subir los informes al sistema SUGO (pide credenciales de Intranet)

### Modo Oculto (Headless)

El switch **🖥️ Modo Oculto (RPA)** en el panel de control permite ejecutar el bot sin mostrar la ventana del navegador:

| Estado | Comportamiento |
|---|---|
| **Desactivado** (default) | El navegador es visible durante la ejecución |
| **Activado** | El RPA corre en segundo plano sin interfaz gráfica del navegador |

---

## 📁 Archivos generados

| Archivo / Carpeta | Ruta | Descripción |
|---|---|---|
| `resultados_procesados.csv` | `dist/` | Registro de resultados por folio (guardado incremental cada 10 folios) |
| `perfil_google_drive/` | `dist/` | Perfil persistente del navegador Chrome con la sesión de Google |
| `Documentos/` | `dist/` | Carpeta donde se colocan los informes a subir al sistema SUGO |

> La carpeta `dist/` se crea automáticamente al iniciar cualquier proceso. Está excluida del repositorio vía `.gitignore`.

---

## 🔑 Columnas requeridas en `Oficios.xlsx`

| Columna | Descripción |
|---|---|
| `Folio Sugo` | Identificador del folio en el sistema SUGO |
| `Folio Wizard` | Identificador de la tarea en el sistema Wizard |
| `Tipo Respuesta` | `positiva` o `negativa` |
| `Selfservice` | Indica si es un folio INE (se omite automáticamente) |
| `Dictamen Wizard` | Dictamen específico para la selección de opciones en Wizard |
| `Informe` | Nombre del archivo de informe ubicado en la carpeta `Documentos/` |

---

## 🛠️ Dependencias principales

| Paquete | Versión mínima | Uso |
|---|---|---|
| `customtkinter` | 5.2.2 | Interfaz gráfica moderna |
| `Pillow` | 10.3.0 | Carga de imágenes en la UI |
| `playwright` | 1.44.0 | Automatización del navegador (RPA) |
| `pandas` | 2.2.0 | Lectura y escritura del archivo Excel |
| `openpyxl` | 3.1.2 | Motor para archivos `.xlsx` |

---

## ⚠️ Notas importantes

- El bot requiere **Google Chrome** instalado en el sistema. No es compatible con Chromium standalone para la sesión persistente de Google.
- Las credenciales de Intranet **no se almacenan** en ningún archivo; se solicitan en cada ejecución del proceso SUGO mediante un diálogo seguro.
- El progreso se guarda automáticamente en `resultados_procesados.csv` cada 10 folios procesados, permitiendo reanudar el proceso si se interrumpe.
