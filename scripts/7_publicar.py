import csv
from datetime import datetime

entrada = "data/silver/ventas_limpias.csv"
fecha_proceso = datetime.now().strftime("%Y%m%d_%H%M%S")
salida = f"data/gold/ventas_gold_{fecha_proceso}.csv"

with open(entrada, encoding="utf-8") as f:
    registros = list(csv.DictReader(f, delimiter=';'))

with open(salida, "w", newline="", encoding="utf-8") as f:
    if registros:
        writer = csv.DictWriter(f, fieldnames=registros[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(registros)

print("=" * 60)
print("PUBLICAR EN PRODUCCIÓN")
print("=" * 60)
print(f"Dataset oficial publicado: {salida}")
print(f"Registros totales listos para análisis: {len(registros)}")