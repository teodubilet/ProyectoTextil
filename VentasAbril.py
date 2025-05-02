#SIMULAMOS LAS VENTAS DE AMBOS LOCALES DEL MES DE ABRIL

import sqlite3
import random
from datetime import date

# Conectar a la base de datos
conn = sqlite3.connect("BBDD Zhoue.db")
cursor = conn.cursor()

# Obtener precios de productos
cursor.execute("SELECT sku, precio FROM Producto")
precios = {sku: precio for sku, precio in cursor.fetchall()}

# Configuración por sucursal
empleados = {
    1: [3, 4, 5],               # San Isidro
    2: [9, 10, 11, 12, 13]      # Unicenter
}

productos = {
    1: [f"ZH{str(i).zfill(3)}" for i in range(1, 85)],     # San Isidro
    2: [f"ZH{str(i).zfill(3)}" for i in range(1, 144)]     # Unicenter
}

talles = [1, 2, 3, 4]
tipos_pago = [1, 2, 3, 4, 5, 6]
abril = [date(2025, 4, d) for d in range(1, 31)]
ventas_por_sucursal = {1: 80, 2: 110}

# Función para crear o recuperar cliente
def obtener_o_crear_cliente(conn, nombre, mail):
    c = conn.cursor()
    c.execute("SELECT id_cliente FROM Cliente WHERE nombre_completo = ? AND mail = ?", (nombre, mail))
    r = c.fetchone()
    if r:
        return r[0]
    c.execute("INSERT INTO Cliente (nombre_completo, mail) VALUES (?, ?)", (nombre, mail))
    conn.commit()
    return c.lastrowid

# Verificar stock
def stock_disponible(conn, sku, talle, sucursal_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cantidad FROM Stock_Local
        WHERE sku_producto = ? AND talle_id = ? AND id_sucursal = ?
    """, (sku, talle, sucursal_id))
    r = cursor.fetchone()
    return r[0] if r else 0

# Registrar venta
def registrar_venta(conn, id_empleado, id_sucursal, id_tipo_pago, productos, fecha):
    cursor = conn.cursor()

    cliente_num = random.randint(1, 80)
    nombre = f"Cliente{cliente_num:03d}"
    mail = f"{nombre.lower()}@ejemplo.com"
    id_cliente = obtener_o_crear_cliente(conn, nombre, mail)

    cursor.execute("""
        INSERT INTO Venta (fecha, id_empleado, id_cliente, id_sucursal, id_tipo_pago)
        VALUES (?, ?, ?, ?, ?)
    """, (fecha.isoformat(), id_empleado, id_cliente, id_sucursal, id_tipo_pago))
    id_venta = cursor.lastrowid

    for p in productos:
        cursor.execute("""
            INSERT INTO Detalle_Venta (id_venta, sku, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
        """, (id_venta, p['sku'], p['cantidad'], p['precio']))

        cursor.execute("""
            UPDATE Stock_Local
            SET cantidad = cantidad - ?
            WHERE sku_producto = ? AND talle_id = ? AND id_sucursal = ?
        """, (p['cantidad'], p['sku'], p['talle'], id_sucursal))

    conn.commit()

# Función principal
def generar_ventas_para_sucursal(sucursal_id, cantidad_ventas):
    exitosas = 0
    fallidas = 0
    while exitosas < cantidad_ventas and fallidas < 300:
        fecha = random.choice(abril)
        if sucursal_id == 1 and fecha.weekday() == 6:  # Domingo
            continue

        id_empleado = random.choice(empleados[sucursal_id])
        id_pago = random.choice(tipos_pago)

        productos_en_venta = []
        usados = set()
        intentos_producto = 0
        cantidad_items = random.randint(1, 3)

        while len(productos_en_venta) < cantidad_items and intentos_producto < 50:
            intentos_producto += 1
            sku = random.choice(productos[sucursal_id])
            if sku in usados:
                continue
            usados.add(sku)
            talle = random.choice(talles)
            cantidad = random.randint(1, 2)

            if stock_disponible(conn, sku, talle, sucursal_id) >= cantidad:
                productos_en_venta.append({
                    'sku': sku,
                    'talle': talle,
                    'cantidad': cantidad,
                    'precio': precios[sku]
                })

        if productos_en_venta:
            registrar_venta(conn, id_empleado, sucursal_id, id_pago, productos_en_venta, fecha)
            exitosas += 1
        else:
            fallidas += 1

    print(f"📍 Sucursal {sucursal_id}: {exitosas} ventas registradas, {fallidas} fallidas por falta de stock.")

# Ejecutar para ambas sucursales
generar_ventas_para_sucursal(1, 80)
generar_ventas_para_sucursal(2, 110)

print("✅ Simulación de ventas finalizada.")

