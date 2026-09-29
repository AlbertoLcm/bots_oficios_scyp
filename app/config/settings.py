import sys
from pathlib import Path

# =========================================
# Files program
# =========================================

IS_FROZEN = getattr(sys, 'frozen', False) # Detecta si es ejecutable Exe o Desarrollo

if IS_FROZEN:
    # INTERNAL_DIR es para los archivos empaquetados con --add-data (como app/assets)
    # Esto funciona igual en Windows y Mac, no hay que cambiarlo.
    INTERNAL_DIR = Path(sys._MEIPASS)
    
    # BASE_DIR es para buscar archivos externos (Oficios.xlsx, usuario_sugo.json)
    exe_path = Path(sys.executable)
    
    if sys.platform == "darwin" and "Contents/MacOS" in str(exe_path):
        # En Mac (.app), subimos niveles: MacOS -> Contents -> main.app -> Carpeta entregable
        BASE_DIR = exe_path.parent.parent.parent.parent
    else:
        # En Windows (.exe), el padre directo es la carpeta entregable
        BASE_DIR = exe_path.parent

else:
    # Entorno de desarrollo
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    INTERNAL_DIR = BASE_DIR

DIST_DIR = BASE_DIR / "dist"
INPUT_FILE = BASE_DIR / "Oficios.xlsx"
ARCHIVO_CREDENCIALES = BASE_DIR / "usuario_sugo.json" 
USER_DATA_DIR = DIST_DIR / "perfil_google_drive"
ASSETS_DIR = INTERNAL_DIR / "app" / "assets"
TEMP_FILE = DIST_DIR / "resultados_temp.csv"
FILE_EXITOS = DIST_DIR / "resultados_procesados.xlsx"

BATCH_GUARDADO = 10

COLUMNS_REQUIRED = [
    "Folio Sugo",
    "Folio Wizard",
    "Tipo Respuesta",
    "Selfservice",
    "Dictamen Wizard",
    "Fecha Cierre"
]

# =========================================
# Params Playwright
# =========================================

URL_WIZARD = "https://bbva-wizardautomexpress-am.appspot.com/welcome-page"
URL_WIZARD_MIS_TAREAS = "https://bbva-wizardautomexpress-am.appspot.com/wizardautomexpr-am/manager/manager-tasks"
URL_SUGO_LOGIN = "https://acprod.intranet.com.mx/mbom_mx_ws/mbom_mx_web/PortalLogon"
URL_CIERRE_OPERACIONES = "https://acprod.intranet.com.mx:443/boixp_mx_web/boixp_mx_web/servlet/ServletOperacionWeb?OPERACION=VGOMX064&LOCALE=es_ES&DATOS_ENTRADA.FLUJO_LANZAR=GOMXFL15240"
URL_SUGO = "https://acprod.intranet.com.mx/mbom_mx_ws/mbom_mx_web/mbom_mx_web_jsp/portal3.jsp"
URL_ASIGNACION_SUGO = "https://acprod.intranet.com.mx:443/boixp_mx_web/boixp_mx_web/servlet/ServletOperacionWeb?OPERACION=VGOMX021&LOCALE=es_ES&DATOS_ENTRADA.FLUJO_LANZAR=GOMXFL13020"
URL_LOGIN_GOOGLE = "https://accounts.google.com/"
URL_ESTATUS_FOLIO = "https://acprod.intranet.com.mx:443/boixp_mx_web/boixp_mx_web/servlet/ServletOperacionWeb?OPERACION=VGOMX012&LOCALE=es_ES&DATOS_ENTRADA.FLUJO_LANZAR=GOMXFL10090"

URL_REPOSITORIO_WIZARD = "acprod.intranet.com.mx"
URL_REPOSITORIO_SUGO = "image-viewer.jsp"

ARGUMENTOS_CHROME = [
    "--ignore-certificate-errors",
    "--disable-blink-features=AutomationControlled",
    "--disable-gpu",
    "--no-sandbox",
    "--no-first-run",             
    "--no-default-browser-check", 
    "--disable-sync",             
    "--disable-popup-blocking",
    "--disable-signin-promo",
    "--disable-features=ChromeSigninInterceptBubble,DiceWebSigninIntercept"
]

# =========================================
# UI program
# =========================================

APP_TITLE = "Bots SCyP"
APP_GEOMETRY = "1000x650"

COLOR_ELECTRIC = "#001391"
COLOR_MIDNIGHT = "#070E46"
COLOR_DARK_BLUE = "#000519"

COLOR_WHITE = "#FFFFFF"
COLOR_SAND = "#F7F8F8"
COLOR_GREEN = "#9CE67E"

COLOR_TEXT_MUTED = "#7A8599"
COLOR_CYAN = "#00E5C0"
COLOR_STATUS_BG = "#EDF8F4"
COLOR_HOVER = "#9FDAFF"