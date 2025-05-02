# ventas_utils.py

# Importamos las librerias correspondientes
import sqlite3
import pandas as pd
from datetime import datetime
import random

# Conectar a la base de datos
def conectar(db_name="BBDD Zhoue.db"):
    return sqlite3.connect(db_name)

# Verificar si un cliente existe; si no, lo crea
def obtener_o_crear_cliente(conn, nombre_completo, mail):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_cliente FROM Cliente WHERE nombre_completo = ? AND mail = ?
    ''', (nombre_completo, mail))
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]
    else:
        cursor.execute('''
            INSERT INTO Cliente (nombre_completo, mail)
            VALUES (?, ?)
        ''', (nombre_completo, mail))
        conn.commit()
        return cursor.lastrowid

# Registrar venta con verificación de stock
def registrar_venta(conn, id_empleado, id_sucursal, id_tipo_pago, productos):
    cursor = conn.cursor()

    # Generar cliente automático
    numero_cliente = random.randint(1, 80)
    nombre_cliente = f"Cliente{numero_cliente:03d}"
    mail_cliente = f"{nombre_cliente.lower()}@ejemplo.com"
    id_cliente = obtener_o_crear_cliente(conn, nombre_cliente, mail_cliente)

    # Insertar en tabla Venta
    fecha_actual = datetime.today().date().isoformat()
    cursor.execute('''
        INSERT INTO Venta (fecha, id_empleado, id_cliente, id_sucursal, id_tipo_pago)
        VALUES (?, ?, ?, ?, ?)
    ''', (fecha_actual, id_empleado, id_cliente, id_sucursal, id_tipo_pago))
    id_venta = cursor.lastrowid

    # Insertar cada producto vendido si hay stock
    for item in productos:
        sku = item["sku"]
        talle = item["talle"]
        cantidad = item["cantidad"]
        precio_unitario = item["precio_unitario"]

        # Verificamos stock disponible
        cursor.execute('''
            SELECT cantidad FROM Stock_Local
            WHERE id_sucursal = ? AND sku_producto = ? AND talle_id = ?
        ''', (id_sucursal, sku, talle))
        resultado = cursor.fetchone()

        if resultado and resultado[0] >= cantidad:
            # Registrar detalle de venta
            cursor.execute('''
                INSERT INTO Detalle_Venta (id_venta, sku, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
            ''', (id_venta, sku, cantidad, precio_unitario))

            # Actualizar stock
            cursor.execute('''
                UPDATE Stock_Local
                SET cantidad = cantidad - ?
                WHERE id_sucursal = ? AND sku_producto = ? AND talle_id = ?
            ''', (cantidad, id_sucursal, sku, talle))

    conn.commit()
    print(f"✅ Venta {id_venta} registrada correctamente.")


