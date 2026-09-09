import customtkinter as ctk
from app.config import settings


class DialogResume(ctk.CTkToplevel):
    """Diálogo modal para preguntar si retomar progreso existente o empezar de cero."""

    def __init__(self, master, callback_resume, callback_fresh, callback_cancel=None):
        super().__init__(master)
        self._callback_resume = callback_resume
        self._callback_fresh = callback_fresh
        self._callback_cancel = callback_cancel

        # Configuración de la ventana
        self.title("Progreso Detectado")
        self.geometry("450x260")
        self.resizable(False, False)
        self.configure(fg_color=settings.COLOR_WHITE)
        self.grab_set()  # Modal
        self.lift()
        self.focus_force()

        # Centrar respecto al padre
        self.after(10, self._centrar)

        # ── Encabezado ──────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=settings.COLOR_ELECTRIC, corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="Progreso Previo Detectado",
            font=ctk.CTkFont(family="Roboto", size=15, weight="bold"),
            text_color="white"
        ).pack(expand=True)

        # ── Mensaje / Descripción ─────────────────────────
        ctk.CTkLabel(
            self,
            text="Se encontró un archivo de resultados con progreso anterior para este Excel.\n\n¿Deseas retomar la ejecución desde el último punto guardado o comenzar todo el proceso de cero?",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color=settings.COLOR_TEXT_MUTED,
            wraplength=400,
            justify="center"
        ).pack(pady=(25, 20), padx=25)

        # ── Botones de Acción ──────────────────────────────
        frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_btns.pack(fill="x", padx=25, pady=(0, 20))

        # Botón Cancelar (Izquierda)
        ctk.CTkButton(
            frame_btns, text="Cancelar", width=90, height=38,
            fg_color="transparent", border_width=1,
            border_color="#CCCCCC", text_color="#555555",
            hover_color="#F0F0F0", corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_cancel
        ).pack(side="left", padx=(0, 10))

        # Botón Empezar de Cero (Centro/Derecha)
        ctk.CTkButton(
            frame_btns, text="Empezar de Cero", width=145, height=38,
            fg_color="#FEE2E2", text_color="#991B1B",
            hover_color="#FCA5A5", corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_fresh
        ).pack(side="left")

        # Botón Retomar (Derecha)
        ctk.CTkButton(
            frame_btns, text="Retomar Progreso", height=38,
            fg_color=settings.COLOR_ELECTRIC, text_color="white",
            hover_color=settings.COLOR_MIDNIGHT, corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_resume
        ).pack(side="right", fill="x", expand=True, padx=(10, 0))

    def _centrar(self):
        master = self.master
        x = master.winfo_x() + (master.winfo_width() // 2) - (450 // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (260 // 2)
        self.geometry(f"+{x}+{y}")

    def _on_resume(self):
        self.grab_release()
        self.destroy()
        if self._callback_resume:
            self._callback_resume()

    def _on_fresh(self):
        self.grab_release()
        self.destroy()
        if self._callback_fresh:
            self._callback_fresh()

    def _on_cancel(self):
        self.grab_release()
        self.destroy()
        if self._callback_cancel:
            self._callback_cancel()
