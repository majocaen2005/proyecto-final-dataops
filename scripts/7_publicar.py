import csv
from datetime import datetime
import psycopg2
import sys

entrada = "data/silver/ventas_limpias.csv"
fecha_proceso = datetime.now().strftime("%Y%m%d_%H%M%S")
salida = f"data/gold/ventas_gold_{fecha_proceso}.csv"

# 1. Leer los datos limpios
with open(entrada, encoding="utf-8") as f:
    registros = list(csv.DictReader(f, delimiter=';'))

# 2. Guardar respaldo en formato CSV
with open(salida, "w", newline="", encoding="utf-8") as f:
    if registros:
        writer = csv.DictWriter(f, fieldnames=registros[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(registros)

# 3. Conexión e Inserción en PostgreSQL
try:
    conn = psycopg2.connect(
        host="localhost",
        port="5433", 
        database="laboratorio",
        user="admin",
        password="admin123"
    )
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas_gold (
        nombre_cliente VARCHAR(100),
        genero VARCHAR(50),
        pais VARCHAR(50),
        precio_usd FLOAT,
        unidades_vendidas INT,
        fecha_venta VARCHAR(50),
        familia_productos VARCHAR(50),
        anio INT,
        ventas_totales FLOAT
    )
    """)
    conn.commit()

    # Limpiar tabla antes de la nueva carga masiva
    cursor.execute("DELETE FROM ventas_gold")
    conn.commit()

    # Insertar los registros limpios
    for row in registros:
        cursor.execute("""
            INSERT INTO ventas_gold (nombre_cliente, genero, pais, precio_usd, unidades_vendidas, fecha_venta, familia_productos, anio, ventas_totales)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Nombre Cliente'],
            row['Genero'],
            row['Pais'],
            float(row['Precio USD']),
            int(row['Unidades Vendidas']),
            row['Fecha Venta'],
            row['Familia de Productos'],
            int(row['Año']),
            float(row['Ventas'])
        ))
    conn.commit()

    cursor.close()
    conn.close()
    print("Datos guardados exitosamente en PostgreSQL (Zona Gold)")

except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
    sys.exit(1)

print("=" * 60)
print("PUBLICAR EN PRODUCCIÓN")
print("=" * 60)
print(f"Dataset oficial publicado en CSV: {salida}")
print(f"Registros totales listos para análisis en Base de Datos: {len(registros)}")