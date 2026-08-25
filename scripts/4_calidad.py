import csv
import json
import sys

with open("data/raw/ventas.csv", encoding="latin1") as f:
    rows = list(csv.DictReader(f, delimiter=';'))

total = len(rows)
errores = []

for index, row in enumerate(rows, start=1):

    # Regla 1: Nombre de Cliente obligatorio
    cliente = row.get("Nombre Cliente")
    if not cliente or str(cliente).strip() == "":
        errores.append(f"Fila {index}: Nombre Cliente vacio")

    # Regla 2: Precio debe ser positivo
    try:
        precio = float(str(row.get("Precio USD", 0)).replace(',', '.'))
        if precio < 0:
            errores.append(f"Fila {index}: Precio USD negativo")
    except ValueError:
        errores.append(f"Fila {index}: Precio USD invalido")

    # Regla 3: Unidades deben ser positivas
    try:
        unidades = int(row.get("Unidades Vendidas", 0))
        if unidades < 0:
            errores.append(f"Fila {index}: Unidades Vendidas negativas")
    except ValueError:
        errores.append(f"Fila {index}: Unidades Vendidas invalidas")
        
    # Regla 4: El año debe ser lógico (mayor a 2000)
    try:
        anio = int(row.get("Año", 0))
        if anio < 2000:
            errores.append(f"Fila {index}: Año fuera de rango logico")
    except ValueError:
        errores.append(f"Fila {index}: Año invalido")

registros_invalidos = len(set(error.split(":")[0] for error in errores))
registros_validos = total - registros_invalidos

quality_score = (registros_validos / total * 100) if total > 0 else 0

resultado = {
    "total_registros": total,
    "registros_validos": registros_validos,
    "registros_invalidos": registros_invalidos,
    "quality_score": round(quality_score, 2),
    "errores_encontrados": len(errores)
}

with open("reports/quality.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)

print("=" * 60)
print("CALIDAD DE DATOS")
print("=" * 60)
print(f"Total registros: {total}")
print(f"Válidos: {registros_validos}")
print(f"Inválidos: {registros_invalidos}")
print(f"SCORE DE CALIDAD: {quality_score:.2f}%")

UMBRAL = 85

if quality_score < UMBRAL:
    print(f"QUALITY GATE FALLÓ: mínimo requerido = {UMBRAL}%")
    sys.exit(1)

print(f"QUALITY GATE APROBADO: mínimo requerido = {UMBRAL}%")