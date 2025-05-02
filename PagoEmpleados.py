import sqlite3
import pandas as pd
import random

# Conexión a la base
conn = sqlite3.connect("BBDD Zhoue.db")
cursor = conn.cursor()

# Parámetros
MES = 4
ANIO = 2025
PAGO_POR_HORA_EXTRA = 2500

# Encargadas por ID (según lo que definiste)
encargadas_ids = [1, 2, 6, 7, 8]

# Obtener todos los empleados
empleados = pd.read_sql_query("SELECT * FROM Empleado", conn)

# Obtener total vendido por cada empleado en abril
ventas_por_empleado = pd.read_sql_query(f"""
    SELECT v.id_empleado, SUM(dv.cantidad * dv.precio_unitario) AS total
    FROM Venta v
    JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
    WHERE strftime('%m', v.fecha) = '{MES:02d}' AND strftime('%Y', v.fecha) = '{ANIO}'
    GROUP BY v.id_empleado
""", conn)
ventas_empleado_dict = dict(zip(ventas_por_empleado.id_empleado, ventas_por_empleado.total))

# Obtener total vendido por sucursal
ventas_por_sucursal = pd.read_sql_query(f"""
    SELECT v.id_sucursal, SUM(dv.cantidad * dv.precio_unitario) AS total
    FROM Venta v
    JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
    WHERE strftime('%m', v.fecha) = '{MES:02d}' AND strftime('%Y', v.fecha) = '{ANIO}'
    GROUP BY v.id_sucursal
""", conn)
ventas_sucursal_dict = dict(zip(ventas_por_sucursal.id_sucursal, ventas_por_sucursal.total))

# Calcular y registrar pago por empleado
for _, row in empleados.iterrows():
    id_empleado = row['id_empleado']
    sueldo_basico = row['sueldo_basico']
    id_sucursal = row['id_sucursal']

    # Horas extra aleatorias (solo algunas personas)
    horas_extra = random.choice([0, 0, 0, random.randint(1, 8)])

    if id_empleado in encargadas_ids:
        comision = round(ventas_sucursal_dict.get(id_sucursal, 0) * 0.015, 2)
    else:
        comision = round(ventas_empleado_dict.get(id_empleado, 0) * 0.008, 2)

    total_pago = sueldo_basico + comision + (horas_extra * PAGO_POR_HORA_EXTRA)

    # Insertar en tabla Pago_Empleado
    cursor.execute("""
        INSERT INTO Pago_Empleado (id_empleado, mes, anio, comision, horas_extra, total_pago)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_empleado, MES, ANIO, comision, horas_extra, total_pago))

conn.commit()
print("✅ Pagos de empleados para abril 2025 registrados correctamente.")
