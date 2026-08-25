import os
import shutil
from datetime import datetime

carpetas = [
    "data/raw",
    "data/silver",
    "data/gold",
    "reports",
    "logs"
]

for carpeta in carpetas:
    os.makedirs(carpeta, exist_ok=True)

for carpeta in ["data/raw", "data/silver", "data/gold", "reports"]:
    for archivo in os.listdir(carpeta):
        ruta = os.path.join(carpeta, archivo)
        if os.path.isfile(ruta):
            os.remove(ruta)
        elif os.path.isdir(ruta):
            shutil.rmtree(ruta)

print("=" * 60)
print("INICIALIZAR")
print("=" * 60)
print(f"Pipeline iniciado: {datetime.now()}")
print(f"Workspace de trabajo: {os.getcwd()}")
print("Entorno preparado correctamente")