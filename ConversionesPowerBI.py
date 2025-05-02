import sqlite3
import pandas as pd

# Conexión a la base
conn = sqlite3.connect("BBDD Zhoue.db")

# Lista de tablas que querés exportar
tablas = [
    "Cliente", "Detalle_Venta", "Empleado", "Pago_Empleado", "Producto",
    "Producto_Talle", "Stock_Local", "Sucursal", "Talle", "Venta", "TipoPago"
]

# Exportar cada tabla a un archivo Excel separado
for tabla in tablas:
    df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
    df.to_excel(f"{tabla}.xlsx", index=False)
    print(f"✅ Tabla '{tabla}' exportada a {tabla}.xlsx")

conn.close()
