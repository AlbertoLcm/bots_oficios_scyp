import customtkinter as ctk
from app.config import preferences, settings


class PanelControls(ctk.CTkFrame):
    def __init__(
            self,
            master,
            image_logo,
            icon_off,
            cmd_asignacion,
            cmd_cierre_oficio,
            cmd_validar_informe,
            cmd_exit,
            cmd_folder_selected
        ):
        
        super().__init__(master, fg_color=settings.COLOR_WHITE, corner_radius=15, border_width=0)

        self.cmd_folder_selected = cmd_folder_selected

        self.lbl_imagen_robot = ctk.CTkLabel(
            self, 
            text="", 
            image=image_logo,
        )
        self.lbl_imagen_robot.pack(pady=(14, 4), padx=20, anchor="w")

        self.lbl_title = ctk.CTkLabel(
            self, text="Bots SCyP",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold"),
            text_color=settings.COLOR_ELECTRIC
        )
        self.lbl_title.pack(pady=(2, 0), padx=20, anchor="w")

        self.lbl_sub = ctk.CTkLabel(
            self, text='Operaciones "Regionales"',
            font=ctk.CTkFont(family="Roboto", size=11),
            text_color=settings.COLOR_TEXT_MUTED
        )
        self.lbl_sub.pack(pady=(0, 2), padx=20, anchor="w")

        self.linea_cian_izq = ctk.CTkFrame(self, width=28, height=2, fg_color=settings.COLOR_CYAN, corner_radius=2)
        self.linea_cian_izq.pack(pady=(2, 8), padx=20, anchor="w")

        # ==========================================
        # --- SECCIÓN CONFIGURACIÓN DE ENTRADAS ---
        # ==========================================
        self.lbl_config_title = ctk.CTkLabel(
            self, text="Configuración de Entrada",
            font=ctk.CTkFont(family="Roboto", size=11, weight="bold"),
            text_color=settings.COLOR_ELECTRIC
        )
        self.lbl_config_title.pack(pady=(4, 2), padx=20, anchor="w")
        
        # --- Selector de Carpeta de Informes ---
        self.frame_folder = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_folder.pack(fill="x", padx=20, pady=2)
        
        self.lbl_folder_title = ctk.CTkLabel(
            self.frame_folder, text="Informes:",
            font=ctk.CTkFont(size=10), text_color=settings.COLOR_TEXT_MUTED
        )
        self.lbl_folder_title.pack(anchor="w")
        
        self.frame_folder_informes = ctk.CTkFrame(self.frame_folder, fg_color="transparent")
        self.frame_folder_informes.pack(fill="x")
        
        self.entry_folder_informes = ctk.CTkEntry(
            self.frame_folder_informes, placeholder_text="Seleccione una carpeta...",
            height=26, corner_radius=6, border_color="#CBD5E1", fg_color="#F8FAFC",
            font=ctk.CTkFont(size=10)
        )
        self.entry_folder_informes.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_folder_informes.configure(state="readonly")
        
        self.btn_browse_folder_informes = ctk.CTkButton(
            self.frame_folder_informes, text="Examinar", width=62, height=26, corner_radius=6,
            fg_color="#F1F5F9", hover_color="#E2E8F0", text_color="#0F172A",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda: self._on_browse_folder("informes")
        )
        self.btn_browse_folder_informes.pack(side="right")

        # --- Selector de Carpeta de INSUMOS ---
        self.frame_folder = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_folder.pack(fill="x", padx=20, pady=2)

        self.lbl_folder_title = ctk.CTkLabel(
            self.frame_folder, text="Insumos:",
            font=ctk.CTkFont(size=10), text_color=settings.COLOR_TEXT_MUTED
        )
        self.lbl_folder_title.pack(anchor="w")

        self.frame_folder_insumos = ctk.CTkFrame(self.frame_folder, fg_color="transparent")
        self.frame_folder_insumos.pack(fill="x")

        self.entry_folder_insumos = ctk.CTkEntry(
            self.frame_folder_insumos, placeholder_text="Seleccione una carpeta...",
            height=26, corner_radius=6, border_color="#CBD5E1", fg_color="#F8FAFC",
            font=ctk.CTkFont(size=10)
        )
        self.entry_folder_insumos.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry_folder_insumos.configure(state="readonly")

        self.btn_browse_folder_insumos = ctk.CTkButton(
            self.frame_folder_insumos, text="Examinar", width=62, height=26, corner_radius=6,
            fg_color="#F1F5F9", hover_color="#E2E8F0", text_color="#0F172A",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda: self._on_browse_folder("insumos")
        )
        self.btn_browse_folder_insumos.pack(side="right")
        
        self.linea_separadora = ctk.CTkFrame(self, height=1, fg_color="#E2E8F0")
        self.linea_separadora.pack(fill="x", padx=20, pady=(8, 6))

        # Botones de Acción usando los Callbacks recibidos por parámetro
        self.btn_asignacion = self.crear_boton(" Autoasignación", cmd_asignacion)
        self.btn_asignacion.pack(pady=3, padx=20, fill="x")

        self.btn_cierre_oficio = self.crear_boton("  Adjuntar Informe / Insumos", cmd_cierre_oficio)
        self.btn_cierre_oficio.pack(pady=3, padx=20, fill="x")

        self.btn_validar_informe = self.crear_boton("  Validar Informe", cmd_validar_informe)
        self.btn_validar_informe.pack(pady=3, padx=20, fill="x")

        self.btn_exit = self.crear_boton_con_imagen("Salir", icon_off, cmd_exit, white=True)
        self.btn_exit.pack(pady=(5, 3), padx=20, fill="x")

        # ==========================================
        # --- OPCIÓN MODO OCULTO (HEADLESS RPA) ---
        # ==========================================
        self.frame_headless = ctk.CTkFrame(
            self,
            fg_color="#F0F4FF",
            corner_radius=8,
            border_width=1,
            border_color="#C5CCE8"
        )
        self.frame_headless.pack(fill="x", padx=20, pady=(3, 4))

        ctk.CTkLabel(
            self.frame_headless,
            text=" Modo Oculto (RPA)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=settings.COLOR_ELECTRIC
        ).pack(side="left", padx=(8, 4), pady=6)

        self._var_headless = ctk.BooleanVar(value=False)
        self.switch_headless = ctk.CTkSwitch(
            self.frame_headless,
            text="",
            variable=self._var_headless,
            onvalue=True,
            offvalue=False,
            width=40,
            progress_color=settings.COLOR_CYAN,
            button_color=settings.COLOR_ELECTRIC,
            button_hover_color=settings.COLOR_MIDNIGHT,
            command=self._on_headless_toggle
        )
        self.switch_headless.pack(side="right", padx=(4, 8), pady=6)

        self.lbl_headless_state = ctk.CTkLabel(
            self.frame_headless,
            text="Desactivado",
            font=ctk.CTkFont(size=9),
            text_color=settings.COLOR_TEXT_MUTED
        )
        self.lbl_headless_state.pack(side="right", padx=(0, 2), pady=6)

        # Espaciador para empujar el estado al fondo
        ctk.CTkFrame(self, fg_color="transparent").pack(expand=True, fill="both")

        # Estado (Caja verde claro)
        self.frame_status = ctk.CTkFrame(self, fg_color=settings.COLOR_STATUS_BG, corner_radius=8, height=34)
        self.frame_status.pack(side="bottom", fill="x", padx=20, pady=10)
        self.frame_status.pack_propagate(False)

        # Ícono Check
        self.lbl_check = ctk.CTkLabel(
            self.frame_status, text="✓", text_color="white", fg_color=settings.COLOR_GREEN,
            width=18, height=18, corner_radius=9, font=ctk.CTkFont(size=10, weight="bold")
        )
        self.lbl_check.pack(side="left", padx=(10, 6), pady=6)

        self.lbl_status = ctk.CTkLabel(
            self.frame_status, text="Estado: Listo", 
            text_color=settings.COLOR_GREEN, font=ctk.CTkFont(size=11, weight="bold")
        )
        self.lbl_status.pack(side="left", pady=6)

    # ==========================================
    # FILE DIALOG CALLBACKS
    # ==========================================
    def _on_browse_folder(self, folder="informes"):
        from tkinter import filedialog

        path = filedialog.askdirectory(
            title=f"Seleccionar carpeta de {folder}", mustexist=True
        )
        if path:
            self.set_default_folder_path(path, folder)
            preferences.save_default_folder_path(path, folder)
            if self.cmd_folder_selected:
                self.cmd_folder_selected(path, folder)

    def set_folder_path(self, path, entry_folder: ctk.CTkEntry):
        entry_folder.configure(state="normal")
        entry_folder.delete(0, "end")
        entry_folder.insert(0, path)
        entry_folder.configure(state="readonly")

    def set_default_folder_path(self, path, folder="informes"):
        entries = {"informes": self.entry_folder_informes, "insumos": self.entry_folder_insumos}
        if path:
            self.set_folder_path(path, entries[folder])

    # ==========================================
    # TOGGLE HEADLESS
    # ==========================================
    def _on_headless_toggle(self):
        activo = self._var_headless.get()
        if activo:
            self.lbl_headless_state.configure(
                text="Activado", text_color=settings.COLOR_ELECTRIC
            )
            self.frame_headless.configure(
                fg_color="#DDE6FF", border_color=settings.COLOR_ELECTRIC
            )
        else:
            self.lbl_headless_state.configure(
                text="Desactivado", text_color=settings.COLOR_TEXT_MUTED
            )
            self.frame_headless.configure(
                fg_color="#F0F4FF", border_color="#C5CCE8"
            )

    def get_modo_oculto(self) -> bool:
        """Devuelve True si el RPA debe ejecutarse en modo headless (sin ventana)."""
        return self._var_headless.get()

    # ==========================================
    # UTILIDADES TRASLADADAS A ESTA CLASE
    # ==========================================
    def crear_boton(self, texto, comando):
        return ctk.CTkButton(
            self, text=texto, command=comando, 
            height=34, corner_radius=8,
            fg_color=settings.COLOR_ELECTRIC, text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            hover_color=settings.COLOR_MIDNIGHT,
            anchor="w"
        )
    
    def crear_boton_con_imagen(self, texto, imagen, comando, white=False):
        return ctk.CTkButton(
            self, 
            text=f"  {texto}",
            image=imagen,
            compound="left",
            command=comando, 
            height=34, 
            corner_radius=8,
            border_color="#334070" if not white else "#CCCCCC",
            border_width=1 if white else 0,
            fg_color=settings.COLOR_ELECTRIC if not white else "white",
            text_color="white" if not white else "black",
            font=ctk.CTkFont(size=12, weight="bold"),
            hover_color="#15337A" if not white else "#E0E0E0",
            anchor="w"
        )

    def cambiar_estado(self, msg, color=settings.COLOR_GREEN, is_processing=False):
        self.lbl_status.configure(text=f"Estado: {msg}", text_color=color)
        if is_processing:
            self.lbl_check.configure(text="●", fg_color="transparent", text_color=color)
        else:
            self.lbl_check.configure(text="✓", fg_color=color, text_color="white")

    def bloquear_ui(self, bloquear):
        estado = "disabled" if bloquear else "normal"
        self.btn_asignacion.configure(state=estado)
        self.btn_cierre_oficio.configure(state=estado)
        self.btn_exit.configure(state=estado)
        self.switch_headless.configure(state=estado)
        self.btn_validar_informe.configure(state=estado)
        self.btn_browse_folder_informes.configure(state=estado)
        self.btn_browse_folder_insumos.configure(state=estado)
