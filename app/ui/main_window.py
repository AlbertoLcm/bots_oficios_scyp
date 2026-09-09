import asyncio
import os
import threading
from pathlib import Path

from PIL import Image
import customtkinter as ctk

from app.config import preferences, settings
from app.core.bots import preparar_entorno, cargar_datos, orchestrator

from app.ui.panel_logs import PanelLogs
from app.ui.panel_controls import PanelControls
from app.ui.panel_grid import PanelGrid
from app.ui.dialog_resume import DialogResume


class BotWizardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.deactivate_automatic_dpi_awareness()
        ctk.set_widget_scaling(1)

        self.img_bbva = ctk.CTkImage(
            Image.open(settings.ASSETS_DIR / "bbva-blue.png"),
            size=(85, 26)
        )

        self.img_bbva_white = ctk.CTkImage(
            Image.open(settings.ASSETS_DIR / "bbva-white.png"),
            size=(53, 16)
        )

        self.icon_security = ctk.CTkImage(
            Image.open(settings.ASSETS_DIR / "security-token-white.png"),
            size=(18, 18)
        )

        self.icon_trash = ctk.CTkImage(
            Image.open(settings.ASSETS_DIR / "trash-white.png"),
            size=(18, 18)
        )

        self.icon_off = ctk.CTkImage(
            Image.open(settings.ASSETS_DIR / "on-off.png"),
            size=(18, 18)
        )

        self.title(settings.APP_TITLE)
        self.geometry("980x620")
        self.minsize(780, 520)
        self.resizable(True, True)
        self.configure(fg_color=settings.COLOR_SAND)

        # Variables de estado
        self.excel_path = None
        self.informes_path = None
        self.insumos_path = None
        # DataFrame cargado en memoria; se reutiliza mientras el programa esté abierto
        self._df = None
        # Columna de status del proceso actualmente en ejecución
        self._col_status_activa: str | None = None
        # Evento para detener la ejecución
        self._cancel_event = threading.Event()

        # Limpiar DIST al iniciar el programa (solo una vez al arrancar)
        preparar_entorno()

        # ==========================================
        # --- INTERFAZ ---
        # ==========================================

        self.grid_columnconfigure(0, weight=3, minsize=280)
        self.grid_columnconfigure(1, weight=7, minsize=480)
        self.grid_rowconfigure(0, weight=4, minsize=200)  # Grid (sin stats usa menos espacio)
        self.grid_rowconfigure(1, weight=6, minsize=260)  # Logs (Terminal ampliada)
        self.grid_rowconfigure(2, weight=0)               # Bottom bar

        # ==========================================
        # --- PANEL IZQUIERDO (CONTROLES) ---
        # ==========================================

        self.panel_izq = PanelControls(
            self,
            image_logo=self.img_bbva,
            icon_off=self.icon_off,
            cmd_asignacion=self.cmd_asignacion,
            cmd_cierre_oficio=self.cmd_cierre_oficio,
            cmd_validar_informe=self.cmd_validar_informe,
            cmd_exit=self.destroy,
            cmd_folder_selected=self.on_folder_selected,
        )
        self.panel_izq.grid(row=0, column=0, rowspan=2, padx=(12, 8), pady=(12, 8), sticky="nsew")

        # ==========================================
        # --- PANEL DERECHO SUPERIOR (GRID) ---
        # ==========================================
        self.panel_grid = PanelGrid(self)
        self.panel_grid.grid(row=0, column=1, padx=(8, 12), pady=(12, 6), sticky="nsew")

        # ==========================================
        # --- PANEL DERECHO INFERIOR (LOGS) ---
        # ==========================================
        self.panel_logs = PanelLogs(
            self, 
            icon_trash=self.icon_trash,
            icon_stop=self.icon_off,
            cmd_stop=self.cmd_detener
        )
        self.panel_logs.grid(row=1, column=1, padx=(8, 12), pady=(6, 8), sticky="nsew")

        # ==========================================
        # --- BARRA INFERIOR (BRANDING) ---
        # ==========================================
        self.panel_bottom = ctk.CTkFrame(self, fg_color=settings.COLOR_DARK_BLUE, height=35, corner_radius=0)
        self.panel_bottom.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.panel_bottom.pack_propagate(False)

        self.lbl_brand_left = ctk.CTkLabel(
            self.panel_bottom, text="  Seguridad  ·  Confianza  ·  Innovación",
            image=self.icon_security, compound="left",
            font=ctk.CTkFont(size=12), text_color="#8997B5"
        )
        self.lbl_brand_left.pack(side="left", padx=20)

        self.lbl_brand_right = ctk.CTkLabel(
            self.panel_bottom, text="  Atención Autoridades  ",
            image=self.img_bbva_white, compound="left",
            font=ctk.CTkFont(size=12), text_color="white"
        )
        self.lbl_brand_right.pack(side="right", padx=20)

        # Cargar datos del Excel de entrada si existe
        if os.path.exists(settings.INPUT_FILE):
            self.excel_path = str(settings.INPUT_FILE)
            self.cargar_datos_excel()

        # Restaurar cada selección; usar las carpetas locales cuando existan.
        for folder in ("informes", "insumos"):
            saved = preferences.load_default_folder_path(folder)
            default = settings.BASE_DIR / folder
            path = Path(saved).expanduser() if saved else default
            if not path.is_dir():
                path = default
            if path.is_dir():
                setattr(self, f"{folder}_path", str(path))
                self.panel_izq.set_default_folder_path(str(path), folder)

        self.panel_logs.agregar_log("Sistema Bots SCyP iniciado correctamente.", success=True)

    # ==========================================
    # HELPERS INTERNOS
    # ==========================================

    def _log(self, msg, **kwargs):
        """Envía un mensaje al panel de logs de forma thread-safe."""
        self.after(0, lambda: self.panel_logs.agregar_log(msg, **kwargs))

    def _set_ui_bloqueada(self, bloqueada: bool):
        """Bloquea o desbloquea la UI (thread-safe)."""
        self.after(0, lambda: self.panel_izq.bloquear_ui(bloqueada))
        self.after(0, lambda: self.panel_logs.set_btn_stop_state(bloqueada))

    def _set_estado(self, msg, color=settings.COLOR_GREEN, is_processing=False):
        """Actualiza el estado inferior (thread-safe)."""
        self.after(0, lambda: self.panel_izq.cambiar_estado(msg, color=color, is_processing=is_processing))

    def _on_proceso_terminado(self):
        """Callback llamado desde el hilo del bot cuando termina (éxito o error)."""
        self._set_ui_bloqueada(False)
        self._set_estado("Listo", color=settings.COLOR_GREEN, is_processing=False)

    def _ejecutar_en_hilo(self, coro):
        """Lanza una coroutine asyncio en un hilo de fondo sin bloquear la UI."""
        def _runner():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(coro)
            finally:
                loop.close()

        hilo = threading.Thread(target=_runner, daemon=True)
        hilo.start()

    def _get_progreso_path(self):
        return str(settings.TEMP_FILE)

    # ==========================================
    # EVENTOS DE LOS BOTONES
    # ==========================================

    def _verificar_progreso_y_ejecutar(self, ejecutar_callback):
        """Verifica si existe un archivo de progreso y ofrece reanudar o empezar de cero."""
        if self._df is None:
            self._log("No hay datos cargados. Verifique que el archivo Oficios.xlsx exista.", error=True)
            return

        progreso_file = self._get_progreso_path()

        if os.path.exists(progreso_file):
            def on_resume():
                self._log("Retomando el progreso anterior...", success=True)
                ejecutar_callback()

            def on_fresh():
                try:
                    os.remove(progreso_file)
                    self._log("Progreso anterior eliminado. Iniciando desde cero...", success=True)
                except Exception as e:
                    self._log(f"No se pudo limpiar el progreso anterior: {e}", error=True)
                # Recargar datos frescos del Excel original
                self.cargar_datos_excel()
                ejecutar_callback()

            def on_cancel():
                self._log("Operación cancelada por el usuario.", warning=True)

            DialogResume(self, callback_resume=on_resume, callback_fresh=on_fresh, callback_cancel=on_cancel)
        else:
            ejecutar_callback()

    def cmd_asignacion(self):
        """Botón Asignación — Asignación de folios en SUGO."""
        def _iniciar():
            if self._df is None:
                self._log("No hay datos cargados.", error=True)
                return
            self._col_status_activa = "Estatus Asignacion"
            modo_oculto = self.panel_izq.get_modo_oculto()
            modo_txt = "oculto (headless)" if modo_oculto else "visible"
            self._log(f"Iniciando proceso de Asignación en modo {modo_txt}...")
            self._set_estado("Ejecutando Asignación...", color=settings.COLOR_CYAN, is_processing=True)
            self._set_ui_bloqueada(True)
            self.after(0, lambda: self.panel_grid.set_col_status_activa(self._col_status_activa))

            self._cancel_event.clear()
            coro = orchestrator(
                df=self._df,
                tipo_tarea="asignacion",
                modo_oculto=modo_oculto,
                log_callback=self._log,
                done_callback=self._on_proceso_terminado,
                informes_dir="",
                status_callback=self._update_row_status,
                cancel_event=self._cancel_event,
            )
            self._ejecutar_en_hilo(coro)

        self._verificar_progreso_y_ejecutar(_iniciar)

    def cmd_validar_informe(self):
        def _iniciar():
            if self._df is None:
                self._log("No hay datos cargados.", error=True)
                return
            self._col_status_activa = "Validacion Informe"
            modo_oculto = self.panel_izq.get_modo_oculto()
            modo_txt = "oculto (headless)" if modo_oculto else "visible"
            self._log(f"Iniciando proceso de Validar Informe en modo {modo_txt}...")
            self._set_estado("Ejecutando Validar Informe...", color=settings.COLOR_CYAN, is_processing=True)
            self._set_ui_bloqueada(True)
            self.after(0, lambda: self.panel_grid.set_col_status_activa(self._col_status_activa))

            self._cancel_event.clear()
            coro = orchestrator(
                df=self._df,
                tipo_tarea="validar_informe",
                modo_oculto=modo_oculto,
                log_callback=self._log,
                done_callback=self._on_proceso_terminado,
                informes_dir="",
                status_callback=self._update_row_status,
                cancel_event=self._cancel_event,
            )
            self._ejecutar_en_hilo(coro)

        self._verificar_progreso_y_ejecutar(_iniciar)


    def cmd_cierre_oficio(self):
        """Botón Cierre Oficio — Flujo combinado: Wizard + adjuntar informe SUGO."""
        for folder in ("informes", "insumos"):
            path = getattr(self, f"{folder}_path")
            if not path or not Path(path).is_dir():
                self._log(f"Seleccione una carpeta válida de {folder} antes de iniciar.", error=True)
                return
        def _iniciar():
            if self._df is None:
                self._log("No hay datos cargados.", error=True)
                return
            self._col_status_activa = "Estatus Wizard"
            modo_oculto = self.panel_izq.get_modo_oculto()
            modo_txt = "oculto (headless)" if modo_oculto else "visible"
            self._log(f"Iniciando Cierre Oficio en modo {modo_txt}...")
            self._set_estado("Ejecutando Cierre Oficio...", color=settings.COLOR_CYAN, is_processing=True)
            self._set_ui_bloqueada(True)
            self.after(0, lambda: self.panel_grid.set_col_status_activa(self._col_status_activa))

            self._cancel_event.clear()
            coro = orchestrator(
                df=self._df,
                tipo_tarea="cierre_oficio",
                modo_oculto=modo_oculto,
                log_callback=self._log,
                done_callback=self._on_proceso_terminado,
                informes_dir=self.informes_path or "",
                insumos_dir=self.insumos_path or "",
                status_callback=self._update_row_status,
                cancel_event=self._cancel_event,
            )
            self._ejecutar_en_hilo(coro)

        self._verificar_progreso_y_ejecutar(_iniciar)

    def cmd_detener(self):
        """Activa el flag de cancelación para detener el proceso en curso."""
        self._log("Señal de detención enviada. Esperando a que el proceso actual finalice su iteración...", warning=True)
        self._cancel_event.set()
        self.panel_logs.set_btn_stop_state(False)

    # ==========================================
    # CALLBACKS DE SELECCIÓN DE ENTRADAS
    # ==========================================

    def on_folder_selected(self, path, folder="informes"):
        setattr(self, f"{folder}_path", path)
        self._log(f"Carpeta de {folder} seleccionada: {path}")

    def cargar_datos_excel(self):
        """Carga el Excel (o el CSV temporal si existe) y lo muestra en el panel de grid.
        
        NO limpia DIST aquí; eso solo ocurre al arrancar el programa.
        Si existe un TEMP_FILE lo usa directamente para reutilizar el progreso de la sesión.
        """
        if not self.excel_path:
            return

        try:
            col_status_default = "Estatus Asignacion"

            df = cargar_datos(log_callback=self._log)

            if df is not None:
                self._df = df  # Guardar referencia en memoria para reutilización en sesión
                self.panel_grid.cargar_datos(df, col_status=col_status_default)
                self._log(f"Se cargaron {len(df)} registros en la tabla.", success=True)
            else:
                self._df = None
                self.panel_grid.limpiar_tabla()
        except Exception as e:
            self._log(f"Error al cargar datos del Excel: {e}", error=True)
            self._df = None
            self.panel_grid.limpiar_tabla()

    def _update_row_status(self, idx, status):
        """Actualiza el estatus de la fila en la tabla de forma segura en el hilo principal."""
        col = self._col_status_activa
        self.after(0, lambda: self.panel_grid.actualizar_estatus(idx, status, col_status=col))