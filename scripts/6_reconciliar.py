import csv
import json
import sys

# Leemos conteos
with open("data/raw/ventas.csv", encoding="latin1") as f:
    raw = list(csv.DictReader(f, delimiter=';'))

with open("data/silver/ventas_limpias.csv", encoding="utf-8") as f:
    silver = list(csv.DictReader(f, delimiter=';'))
    
# Leemos cuántos errores identificó la fase de Calidad
with open("reports/quality.json", encoding="utf-8") as f:
    quality = json.load(f)

raw_count = len(raw)
silver_count = len(silver)
invalidos_esperados = quality["registros_invalidos"]

# Ecuación de reconciliación
reconciled = (raw_count == silver_count + invalidos_esperados)

resultado = {
    "raw_count": raw_count,
    "silver_count": silver_count,
    "invalidos_eliminados": invalidos_esperados,
    "reconciled": reconciled
}

with open("reports/reconciliation.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4)

print("=" * 60)
print("RECONCILIACIÓN")
print("=" * 60)
print(f"Registros extraídos (RAW): {raw_count}")
print(f"Registros limpios (SILVER): {silver_count}")
print(f"Registros eliminados: {invalidos_esperados}")

if not reconciled:
    print("RECONCILIACIÓN FALLÓ: Se perdieron registros de forma inexplicable.")
    sys.exit(1)

print("RECONCILIACIÓN APROBADA: El flujo de datos cuadra perfectamente.")