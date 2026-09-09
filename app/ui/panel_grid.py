import customtkinter as ctk
from tkinter import ttk

# Fallback en caso de importación modular local
try:
    from app.config import settings
except ImportError:
    class SettingsFallback:
        COLOR_WHITE = "#FFFFFF"
        COLOR_ELECTRIC = "#2563EB"
        COLOR_TEXT_MUTED = "#64748B"
    settings = SettingsFallback()


class PanelGrid(ctk.CTkFrame):
    """Componente de tabla interactiva con resumen de progreso (Stats) integrado sin emojis."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=settings.COLOR_WHITE,
            corner_radius=15,
            border_width=1,
            border_color="#E2E8F0",
            **kwargs
        )

        # --- Cabecera Panel ---
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(fill="x", padx=25, pady=(18, 10))

        # Contenedor título e información básica (Fila Superior)
        self.frame_title_box = ctk.CTkFrame(self.frame_header, fg_color="transparent")
        self.frame_title_box.pack(fill="x", anchor="w")

        self.lbl_title = ctk.CTkLabel(
            self.frame_title_box,
            text="Registros Cargados (Excel)",
            font=ctk.CTkFont(family="Roboto", size=17, weight="bold"),
            text_color=settings.COLOR_ELECTRIC
        )
        self.lbl_title.pack(side="left")

        self.lbl_count = ctk.CTkLabel(
            self.frame_title_box,
            text="0 registros",
            font=ctk.CTkFont(family="Roboto", size=11, weight="bold"),
            text_color=settings.COLOR_TEXT_MUTED,
            fg_color="#F1F5F9",
            corner_radius=6,
            padx=8,
            pady=2
        )
        self.lbl_count.pack(side="left", padx=12)

        # Contenedor de Estadísticas Compactas sin Emojis (Debajo del Título)
        self.frame_stats = ctk.CTkFrame(self.frame_header, fg_color="transparent")
        self.frame_stats.pack(fill="x", anchor="w", pady=(8, 0))

        # Badges limpios y compactos para resumen visual de progreso
        self.badge_labels = {}
        badges_config = [
            ("pendientes", "Pendientes: 0", "#475569", "#F1F5F9"),
            ("procesando", "Procesando: 0", "#1D4ED8", "#EFF6FF"),
            ("completados", "Completados: 0", "#065F46", "#F0FDF4"),
            ("warnings", "Advertencias: 0", "#92400E", "#FEF3C7"),
            ("errores", "Errores: 0", "#991B1B", "#FEF2F2")
        ]

        for key, initial_text, text_col, bg_col in badges_config:
            lbl = ctk.CTkLabel(
                self.frame_stats,
                text=initial_text,
                font=ctk.CTkFont(family="Roboto", size=11, weight="bold"),
                text_color=text_col,
                fg_color=bg_col,
                corner_radius=6,
                padx=8,
                pady=2
            )
            # Primer badge alineado al margen izquierdo del título
            pad_x = (0, 6) if key == "pendientes" else (0, 6)
            lbl.pack(side="left", padx=pad_x)
            self.badge_labels[key] = lbl

        # Línea divisoria superior
        self.linea_decorativa = ctk.CTkFrame(self, height=1, fg_color="#E2E8F0")
        self.linea_decorativa.pack(fill="x", padx=25, pady=(0, 10))

        # --- Contenedor de la Tabla ---
        self.frame_table = ctk.CTkFrame(self, fg_color="transparent", border_width=0)
        self.frame_table.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Estilos ttk (se definen una sola vez)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Custom.Treeview",
            background=settings.COLOR_WHITE,
            foreground="#1E293B",
            rowheight=35,
            fieldbackground=settings.COLOR_WHITE,
            font=("Roboto", 11),
            border_width=0
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            background="#F8FAFC",
            foreground="#475569",
            font=("Roboto", 11, "bold"),
            relief="flat"
        )
        self.style.map(
            "Custom.Treeview.Heading",
            background=[("active", "#E2E8F0")],
            foreground=[("active", "#0F172A")]
        )
        self.style.map(
            "Custom.Treeview",
            background=[("selected", "#EFF6FF")],
            foreground=[("selected", "#1D4ED8")]
        )

        # Estado interno
        self.tree = None
        self.scrollbar_y = None
        self.scrollbar_x = None
        self.row_items = {}  # idx pandas → item_id Treeview
        self._tree_cols = []
        self.col_status_activa = "Estatus Asignacion"

        # Treeview vacío de arranque
        self._rebuild_tree(["Estatus Asignacion", "Estatus Wizard", "Estatus Informe"])

    def _rebuild_tree(self, cols: list):
        """Destruye el Treeview existente y crea uno nuevo con las columnas dadas."""
        if self.tree:
            self.tree.destroy()
        if self.scrollbar_y:
            self.scrollbar_y.destroy()
        if self.scrollbar_x:
            self.scrollbar_x.destroy()

        self._tree_cols = list(cols)

        self.tree = ttk.Treeview(
            self.frame_table,
            columns=self._tree_cols,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        # Scrollbars
        self.scrollbar_y = ctk.CTkScrollbar(
            self.frame_table, orientation="vertical", command=self.tree.yview
        )
        self.scrollbar_x = ctk.CTkScrollbar(
            self.frame_table, orientation="horizontal", command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set
        )

        # Layout: X abajo → Y derecha → Treeview ocupa el resto
        self.scrollbar_x.pack(side="bottom", fill="x", pady=(2, 0))
        self.scrollbar_y.pack(side="right", fill="y", padx=(5, 0))
        self.tree.pack(side="left", fill="both", expand=True)

        # Configurar columnas
        for col in self._tree_cols:
            if col.startswith("Estatus"):
                self.tree.heading(col, text=col, anchor="center")
                self.tree.column(col, width=130, minwidth=90, anchor="center", stretch=False)
            else:
                w = self._ancho_columna(col)
                self.tree.heading(col, text=col, anchor="w")
                self.tree.column(col, width=w, minwidth=80, anchor="w", stretch=False)

        # Tags de estilo
        self.tree.tag_configure("evenrow", background=settings.COLOR_WHITE)
        self.tree.tag_configure("oddrow", background="#F8FAFC")
        self.tree.tag_configure("status_pendiente", foreground="#475569", background=settings.COLOR_WHITE)
        self.tree.tag_configure("status_procesando", foreground="#1D4ED8", background="#EFF6FF")
        self.tree.tag_configure("status_completado", foreground="#065F46", background="#F0FDF4")
        self.tree.tag_configure("status_error", foreground="#991B1B", background="#FEF2F2")
        self.tree.tag_configure("status_warning", foreground="#92400E", background="#FEF3C7")

    @staticmethod
    def _ancho_columna(col: str) -> int:
        anchos = {
            "Folio Sugo": 110,
            "Folio Wizard": 120,
            "Tipo Respuesta": 220,
            "Selfservice": 130,
            "Dictamen Wizard": 220,
            "Informe": 200,
            "Fecha Cierre": 110,
        }
        return anchos.get(col, 140)

    def _tag_para_status(self, status: str, row_index: int) -> str:
        s = str(status).strip().lower()
        if "pendiente" in s or s in ("", "none", "nan"):
            return "status_pendiente"
        if "procesando" in s or "ejecutando" in s:
            return "status_procesando"
        if "completado" in s or s == "ok":
            return "status_completado"
        if "error" in s:
            return "status_error"
        if "no encontrado" in s or "omitido" in s or "faltante" in s or "warning" in s:
            return "status_warning"
        return "evenrow" if row_index % 2 == 0 else "oddrow"

    def _clasificar_status(self, status: str) -> str:
        """Categoriza un texto de estatus en una clave para el conteo de estadísticas."""
        s = str(status).strip().lower()
        if "pendiente" in s or s in ("", "none", "nan"):
            return "pendientes"
        if "procesando" in s or "ejecutando" in s:
            return "procesando"
        if "completado" in s or s == "ok":
            return "completados"
        if "error" in s:
            return "errores"
        if "no encontrado" in s or "omitido" in s or "faltante" in s or "warning" in s:
            return "warnings"
        return "pendientes"

    def _actualizar_resumen_stats(self):
        """Calcula y actualiza dinámicamente el conteo de badges de progreso (sin emojis)."""
        col = self.col_status_activa
        if not col or col not in self._tree_cols or not self.tree:
            return

        col_idx = self._tree_cols.index(col)
        counts = {
            "pendientes": 0,
            "procesando": 0,
            "completados": 0,
            "warnings": 0,
            "errores": 0
        }

        # Recorrer las filas visibles para recalcular estatus
        for item_id in self.tree.get_children():
            vals = self.tree.item(item_id, "values")
            if len(vals) > col_idx:
                status_val = vals[col_idx]
                categoria = self._clasificar_status(status_val)
                counts[categoria] += 1

        # Actualizar etiquetas de texto limpias sin emojis
        self.badge_labels["pendientes"].configure(text=f"Pendientes: {counts['pendientes']}")
        self.badge_labels["procesando"].configure(text=f"Procesando: {counts['procesando']}")
        self.badge_labels["completados"].configure(text=f"Completados: {counts['completados']}")
        self.badge_labels["warnings"].configure(text=f"Advertencias: {counts['warnings']}")
        self.badge_labels["errores"].configure(text=f"Errores: {counts['errores']}")

    def set_col_status_activa(self, col_status: str):
        """Cambia la columna de status activa y refresca el resumen visual."""
        self.col_status_activa = col_status
        self._actualizar_resumen_stats()

    def cargar_datos(self, df, col_status: str = None):
        """Reconstruye la tabla con TODAS las columnas del DataFrame e inicializa las stats."""
        self.col_status_activa = col_status or self.col_status_activa
        self.row_items.clear()

        if df is None or df.empty:
            self.lbl_count.configure(text="0 registros")
            self._rebuild_tree(["Estatus Asignacion", "Estatus Wizard", "Estatus Informe"])
            self._actualizar_resumen_stats()
            return

        # Organizar columnas: Los tres Estatus primero, luego el resto
        status_cols = ["Estatus Asignacion", "Estatus Wizard", "Estatus Informe"]
        status_cols = [c for c in status_cols if c in df.columns]
        data_cols = [c for c in df.columns if c not in status_cols]

        self._tree_cols = status_cols + data_cols

        # Reconstruir Treeview
        self._rebuild_tree(self._tree_cols)
        self.lbl_count.configure(text=f"{len(df)} registros")

        col_stat = self.col_status_activa
        if not col_stat or col_stat not in df.columns:
            if status_cols:
                col_stat = status_cols[0]
                self.col_status_activa = col_stat

        # Insertar registros
        for idx, row in df.iterrows():
            val_status = str(row.get(col_stat, "Pendiente")).strip() if col_stat else "Pendiente"

            data_vals = []
            for col in self._tree_cols:
                v = str(row.get(col, "")).strip()
                if v.endswith(".0"):
                    v = v[:-2]
                data_vals.append(v)

            item_id = self.tree.insert("", "end", values=tuple(data_vals))
            self.row_items[idx] = item_id
            self.tree.item(item_id, tags=(self._tag_para_status(val_status, idx),))

        # Recalcular indicadores
        self._actualizar_resumen_stats()

    def actualizar_estatus(self, row_index, nuevo_estatus, col_status: str = None):
        """Actualiza la columna de Estatus de una fila en tiempo real y refresca las stats."""
        if row_index not in self.row_items:
            return

        item_id = self.row_items[row_index]
        valores = list(self.tree.item(item_id, "values"))

        col = col_status or self.col_status_activa
        if col in self._tree_cols:
            col_idx = self._tree_cols.index(col)
            # Asegurar longitud suficiente de la lista de valores
            while len(valores) <= col_idx:
                valores.append("")

            valores[col_idx] = nuevo_estatus
            self.tree.item(item_id, values=valores)

            # Solo cambiar el tag si estamos actualizando la columna activa
            if col == self.col_status_activa:
                self.tree.item(item_id, tags=(self._tag_para_status(nuevo_estatus, row_index),))

            self.tree.see(item_id)
            self.tree.selection_set(item_id)

            # Actualizar resumen de progreso
            self._actualizar_resumen_stats()

    def limpiar_tabla(self):
        """Elimina todas las filas de la tabla y resetea las estadísticas."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.row_items.clear()
        self.lbl_count.configure(text="0 registros")
        self._actualizar_resumen_stats()