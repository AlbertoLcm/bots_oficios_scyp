import datetime
import customtkinter as ctk
from app.config import settings


class PanelLogs(ctk.CTkFrame):
    def __init__(self, master, icon_trash, icon_stop=None, cmd_stop=None):
        # Inicializamos el Frame con los colores de settings
        super().__init__(master, fg_color=settings.COLOR_MIDNIGHT, corner_radius=15)
        
        # --- Cabecera Panel Derecho ---
        self.frame_log_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_log_header.pack(fill="x", padx=30, pady=(30, 15))

        self.lbl_log_title = ctk.CTkLabel(
            self.frame_log_header, text="Registro de Actividad", 
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),
            text_color="white"
        )
        self.lbl_log_title.pack(side="left")

        # Botón Limpiar y línea decorativa
        self.btn_clear = ctk.CTkButton(
            self.frame_log_header, text="Limpiar", width=80, height=28,
            image=icon_trash, compound="left",
            fg_color="transparent", border_width=1, border_color="#334070",
            hover_color="#1A2859", text_color="#A2ADC0",
            command=self.limpiar_logs
        )
        self.btn_clear.pack(side="right", padx=(15, 0))

        if icon_stop and cmd_stop:
            self.btn_stop = ctk.CTkButton(
                self.frame_log_header, text="Detener", width=80, height=28,
                fg_color="#e6b8af", border_width=1, border_color="#a61c00",
                hover_color="#dd7e6b", text_color="#a61c00",
                text_color_disabled="#a61c00",
                command=cmd_stop, corner_radius=8,
                state="disabled" # Starts disabled
            )
            self.btn_stop.pack(side="right", padx=(15, 0))

        self.linea_cian_der = ctk.CTkFrame(self.frame_log_header, width=30, height=3, fg_color=settings.COLOR_CYAN, corner_radius=2)
        self.linea_cian_der.pack(side="right")

        # --- Terminal de Logs ---
        self.txt_logs = ctk.CTkTextbox(
            self, 
            font=ctk.CTkFont(family="Courier New", size=13),
            fg_color="transparent",
            text_color="#C4CDD5",
            wrap="word"
        )
        self.txt_logs.pack(padx=25, pady=(0, 25), fill="both", expand=True)
        
        # Configuración de colores en el texto (Tags)
        self.txt_logs.tag_config("cyan_dot", foreground=settings.COLOR_CYAN)
        self.txt_logs.tag_config("success", foreground=settings.COLOR_GREEN)
        self.txt_logs.tag_config("error", foreground="#FF6B6B")
        self.txt_logs.tag_config("warning", foreground="#FFA552")
        self.txt_logs.tag_config("timestamp", foreground="#7A8599")
        self.txt_logs.configure(state="disabled")

    # --- Métodos propios del panel ---
    def agregar_log(self, texto, success=False, error=False, warning=False):
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.txt_logs.configure(state="normal")
        
        if success:
            self.txt_logs.insert("end", "  ✓ ", "success")
        elif error:
            self.txt_logs.insert("end", "  ✗ ", "error")
        elif warning:
            self.txt_logs.insert("end", "  ⚠ ", "warning")
        else:
            self.txt_logs.insert("end", "  ● ", "cyan_dot")
            
        self.txt_logs.insert("end", f"[{hora}] ", "timestamp")
        
        if success:
            self.txt_logs.insert("end", f"{texto}\n", "success")
        elif error:
            self.txt_logs.insert("end", f"{texto}\n", "error")
        elif warning:
            self.txt_logs.insert("end", f"{texto}\n", "warning")
        else:
            self.txt_logs.insert("end", f"{texto}\n")
            
        self.txt_logs.configure(state="disabled")
        self.txt_logs.see("end")

    def limpiar_logs(self):
        self.txt_logs.configure(state="normal")
        self.txt_logs.delete("1.0", "end")
        self.txt_logs.configure(state="disabled")
        self.agregar_log("Registro limpiado.", success=True)

    def set_btn_stop_state(self, is_running: bool):
        if hasattr(self, 'btn_stop'):
            self.btn_stop.configure(state="normal" if is_running else "disabled")