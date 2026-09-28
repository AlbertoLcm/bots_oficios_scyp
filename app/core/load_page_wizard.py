from playwright.async_api import async_playwright, BrowserContext, Page, Playwright, TimeoutError as PlaywrightTimeoutError
import re
import sys
from pathlib import Path

URL_WIZARD = "https://bbva-wizardautomexpress-am.appspot.com/welcome-page"
URL_LOGIN_GOOGLE = "https://accounts.google.com/"

IS_FROZEN = getattr(sys, 'frozen', False) # Detecta si es ejecutable Exe o Desarrollo

if IS_FROZEN:
    BASE_DIR = Path(sys.executable).parent
    
    INTERNAL_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    INTERNAL_DIR = BASE_DIR

DIST_DIR = BASE_DIR / "dist"
INPUT_FILE = BASE_DIR / "Oficios.xlsx"
ARCHIVO_CREDENCIALES = "usuario_sugo.json" 
USER_DATA_DIR = DIST_DIR / "perfil_google_drive"
ASSETS_DIR = INTERNAL_DIR / "app" / "assets"
TEMP_FILE = DIST_DIR / "resultados_temp.csv"
FILE_EXITOS = DIST_DIR / "resultados_procesados.xlsx"

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

async def load_page_wizard(context: BrowserContext, p: Playwright, headless: bool):
    page_wizard = await context.new_page()

    await page_wizard.goto(URL_WIZARD, timeout=10_000)
    await page_wizard.wait_for_load_state(state="domcontentloaded")

    if 'idp/profile' in page_wizard.url or 'accounts.google' in page_wizard.url:
        await context.close()

        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            channel="chrome",
            args=ARGUMENTOS_CHROME
        )
        page_login = context.pages[0] if context.pages else await context.new_page()

        await page_login.goto(URL_LOGIN_GOOGLE, timeout=10_000)
        await page_login.wait_for_load_state(state="domcontentloaded")

        await page_login.wait_for_url(re.compile(r"myaccount"), timeout=0)
        
        await context.close()

        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=headless,
            channel="chrome",
            args=ARGUMENTOS_CHROME
        )
        page_wizard = context.pages[0] if context.pages else await context.new_page()
        
        await page_wizard.goto(URL_WIZARD, timeout=10_000)
        await page_wizard.wait_for_load_state(state="domcontentloaded")

    if not 'welcome-page' in page_wizard.url:
        return context, None

    return context, page_wizard