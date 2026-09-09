import os
import pandas as pd
from app.config import settings
from app.ui.main_window import BotWizardApp


def main():
    # Asegurar que el excel de entrada exista en la raíz del proyecto
    ruta_excel = settings.INPUT_FILE
    if not os.path.exists(ruta_excel):
        cols = ["Folio Sugo", "Folio Wizard", "Tipo Respuesta", "Selfservice", "Dictamen Wizard", "Informe", "Fecha Cierre"]
        df = pd.DataFrame(columns=cols)
        df.to_excel(ruta_excel, index=False)
        print(f"Archivo Excel inicial creado en: {ruta_excel}")

    app = BotWizardApp()
    app.mainloop()


if __name__ == "__main__":
    main()