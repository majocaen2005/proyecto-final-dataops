import csv
import json
from collections import Counter
import sys

archivo = "data/raw/ventas.csv"

try:
    with open(archivo, encoding="latin1") as f:
        rows = list(csv.DictReader(f, delimiter=';'))
except Exception as e:
    print(f"Error al leer {archivo}: {e}")
    sys.exit(1)

total = len(rows)

# Conteo de nulos por columna
nulls = {
    column: sum(
        1 for row in rows
        if not row.get(column) or str(row.get(column)).strip() == ""
    )
    for column in rows[0].keys()
}

# Conteo de filas exactamente duplicadas (todas las columnas iguales)
filas_unicas = set(tuple(row.items()) for row in rows)
duplicados = total - len(filas_unicas)

# Distribución de productos vendidos
familias = Counter(row.get("Familia de Productos") for row in rows)

profile = {
    "total_registros": total,
    "filas_duplicadas": duplicados,
    "valores_nulos": nulls,
    "distribucion_familias": dict(familias)
}

with open("reports/profile.json", "w", encoding="utf-8") as f:
    json.dump(profile, f, indent=4, ensure_ascii=False)

print("=" * 60)
print("PERFILAR DATOS")
print("=" * 60)
print(f"Total registros: {total}")
print(f"Filas duplicadas exactas: {duplicados}")
print(f"Nulos encontrados totales: {sum(nulls.values())}")
print("Reporte generado: reports/profile.json")