import shutil
import os
import sys
from datetime import datetime

archivo_origen = "ventas_electronica_parcial.csv"
archivo_destino = "data/raw/ventas.csv"

print("=" * 60)
print("EXTRAER")
print("=" * 60)

if not os.path.exists(archivo_origen):
    print(f"ERROR FATAL: No se encontró el archivo '{archivo_origen}'.")
    sys.exit(1)

# Copiar el archivo a la zona RAW
shutil.copy2(archivo_origen, archivo_destino)

# Contar registros con la codificación correcta (ignorando la cabecera)
try:
    with open(archivo_destino, encoding="latin1") as f:
        registros = sum(1 for row in f) - 1
except Exception as e:
    print(f"Error al leer el archivo extraído: {e}")
    sys.exit(1)

print(f"Fecha: {datetime.now()}")
print(f"Archivo origen: {archivo_origen}")
print(f"Registros extraídos: {registros}")
print(f"Archivo destino preparado en: {archivo_destino}")