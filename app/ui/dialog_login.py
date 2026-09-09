import customtkinter as ctk
from app.config import settings


class DialogLogin(ctk.CTkToplevel):
    """Diálogo modal para capturar credenciales de la Intranet (SUGO)."""

    def __init__(self, master, callback_ok, callback_cancel=None):
        super().__init__(master)
        self._callback_ok = callback_ok
        self._callback_cancel = callback_cancel

        # Configuración de la ventana
        self.title("Autenticación Intranet")
        self.geometry("380x330")
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
            header, text="🔐  Credenciales Intranet",
            font=ctk.CTkFont(family="Roboto", size=15, weight="bold"),
            text_color="white"
        ).pack(expand=True)

        # ── Subtítulo ────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="Ingresa tus datos para acceder al sistema SUGO",
            font=ctk.CTkFont(size=12),
            text_color=settings.COLOR_TEXT_MUTED,
            wraplength=330
        ).pack(pady=(18, 4), padx=25, anchor="w")

        # ── Campo Usuario ────────────────────────────────
        ctk.CTkLabel(
            self, text="Usuario", font=ctk.CTkFont(size=13, weight="bold"),
            text_color=settings.COLOR_ELECTRIC
        ).pack(padx=25, anchor="w")

        self.entry_user = ctk.CTkEntry(
            self, placeholder_text="Ej. nombre.apellido",
            height=38, corner_radius=8,
            border_color=settings.COLOR_ELECTRIC, border_width=1,
            font=ctk.CTkFont(size=13)
        )
        self.entry_user.pack(fill="x", padx=25, pady=(4, 10))

        # ── Campo Contraseña ─────────────────────────────
        ctk.CTkLabel(
            self, text="Contraseña", font=ctk.CTkFont(size=13, weight="bold"),
            text_color=settings.COLOR_ELECTRIC
        ).pack(padx=25, anchor="w")

        self.entry_pass = ctk.CTkEntry(
            self, placeholder_text="••••••••",
            show="•", height=38, corner_radius=8,
            border_color=settings.COLOR_ELECTRIC, border_width=1,
            font=ctk.CTkFont(size=13)
        )
        self.entry_pass.pack(fill="x", padx=25, pady=(4, 18))
        self.entry_pass.bind("<Return>", lambda e: self._on_ok())

        # ── Botones ──────────────────────────────────────
        frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_btns.pack(fill="x", padx=25, pady=(0, 20))

        ctk.CTkButton(
            frame_btns, text="Cancelar", width=100, height=38,
            fg_color="transparent", border_width=1,
            border_color="#CCCCCC", text_color="#555555",
            hover_color="#F0F0F0", corner_radius=8,
            command=self._on_cancel
        ).pack(side="left")

        ctk.CTkButton(
            frame_btns, text="Iniciar Sesión", height=38,
            fg_color=settings.COLOR_ELECTRIC, text_color="white",
            hover_color=settings.COLOR_MIDNIGHT, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_ok
        ).pack(side="right")

        self.entry_user.focus()

    def _centrar(self):
        master = self.master
        x = master.winfo_x() + (master.winfo_width() // 2) - (380 // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (330 // 2)
        self.geometry(f"+{x}+{y}")

    def _on_ok(self):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get()
        if not user or not password:
            self.entry_user.configure(border_color="red" if not user else settings.COLOR_ELECTRIC)
            self.entry_pass.configure(border_color="red" if not password else settings.COLOR_ELECTRIC)
            return
        self.grab_release()
        self.destroy()
        self._callback_ok(user, password)

    def _on_cancel(self):
        self.grab_release()
        self.destroy()
        if self._callback_cancel:
            self._callback_cancel()
