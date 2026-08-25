import csv
import os

entrada = "data/raw/ventas.csv"
salida = "data/silver/ventas_limpias.csv"

resultado = []
registros_descartados = 0

with open(entrada, encoding="latin1") as f:
    for row in csv.DictReader(f, delimiter=';'):
        
        # 1. Filtro de Limpieza (Reglas de Calidad)
        cliente = row.get("Nombre Cliente", "").strip()
        try:
            precio = float(str(row.get("Precio USD", 0)).replace(',', '.'))
        except ValueError:
            precio = -1
        try:
            unidades = int(row.get("Unidades Vendidas", 0))
        except ValueError:
            unidades = -1
        try:
            anio = int(row.get("Año", 0))
        except ValueError:
            anio = -1

        # Si la fila tiene errores críticos, la ignoramos (se elimina)
        if not cliente or precio < 0 or unidades < 0 or anio < 2000:
            registros_descartados += 1
            continue

        # 2. Transformaciones de Negocio
        # Imputar género faltante
        genero = row.get("Genero", "").strip()
        if not genero:
            genero = "No especificado"
            
        # Estandarizar textos de países (ej. "perú" -> "Perú")
        pais = row.get("Pais", "").strip().title()

        # Recalcular la columna de ventas totales para evitar fraude/errores
        ventas_calculadas = round(precio * unidades, 2)

        # 3. Guardar fila limpia
        row["Nombre Cliente"] = cliente
        row["Genero"] = genero
        row["Pais"] = pais
        row["Precio USD"] = precio
        row["Unidades Vendidas"] = unidades
        row["Año"] = anio
        row["Ventas"] = ventas_calculadas

        resultado.append(row)

# Guardamos con estándar UTF-8 para producción
with open(salida, "w", newline="", encoding="utf-8") as f:
    if resultado:
        writer = csv.DictWriter(f, fieldnames=resultado[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(resultado)

print("=" * 60)
print("TRANSFORMAR Y LIMPIAR")
print("=" * 60)
print(f"Registros limpios guardados en SILVER: {len(resultado)}")
print(f"Registros corruptos descartados: {registros_descartados}")