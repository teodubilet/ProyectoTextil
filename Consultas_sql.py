# 1. Total de ventas del local San Isidro en abril
#ELECT SUM(dv.cantidad * dv.precio_unitario) AS total_ventas_san_isidro
#FROM Venta v
#JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
#WHERE v.id_sucursal = 1 AND strftime('%Y-%m', v.fecha) = '2025-04';

# 2. Total de ventas del local Unicenter en abril
#SELECT SUM(dv.cantidad * dv.precio_unitario) AS total_ventas_unicenter
#FROM Venta v
#JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
#WHERE v.id_sucursal = 2 AND strftime('%Y-%m', v.fecha) = '2025-04';

# 3. Ticket promedio por venta (San Isidro)
#SELECT AVG(total) AS ticket_promedio
#FROM (
#  SELECT SUM(dv.cantidad * dv.precio_unitario) AS total
#  FROM Venta v
#  JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
#  WHERE v.id_sucursal = 1 AND strftime('%Y-%m', v.fecha) = '2025-04'
#  GROUP BY v.id_venta
#);

# 4. Productos más vendidos en San Isidro
#SELECT p.nombre, SUM(dv.cantidad) AS unidades_vendidas
#FROM Detalle_Venta dv
#JOIN Producto p ON dv.sku = p.sku
#JOIN Venta v ON v.id_venta = dv.id_venta
#WHERE v.id_sucursal = 1 AND strftime('%Y-%m', v.fecha) = '2025-04'
#GROUP BY p.nombre
#ORDER BY unidades_vendidas DESC
#LIMIT 10;

# 5. Medio de pago más utilizado en abril
#SELECT tp.descripcion, COUNT(*) AS cantidad
#FROM Venta v
#JOIN TipoPago tp ON v.id_tipo_pago = tp.id_tipo_pago
#WHERE strftime('%Y-%m', v.fecha) = '2025-04'
#GROUP BY tp.descripcion
#ORDER BY cantidad DESC;

# 6. Clientes que más gastaron
#SELECT c.nombre_completo, SUM(dv.cantidad * dv.precio_unitario) AS total_gastado
#FROM Venta v
#JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
#JOIN Cliente c ON v.id_cliente = c.id_cliente
#WHERE strftime('%Y-%m', v.fecha) = '2025-04'
#GROUP BY c.nombre_completo
#ORDER BY total_gastado DESC
#LIMIT 5;

# 7. Total de productos vendidos por sucursal
#SELECT s.nombre, SUM(dv.cantidad) AS total_productos
#FROM Venta v
#JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
#JOIN Sucursal s ON v.id_sucursal = s.id_sucursal
#WHERE strftime('%Y-%m', v.fecha) = '2025-04'
#GROUP BY s.nombre;

# 8. Ventas por día en San Isidro
#SELECT v.fecha, SUM(dv.cantidad * dv.precio_unitario) AS total
#FROM Venta v
#JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
#WHERE v.id_sucursal = 1 AND strftime('%Y-%m', v.fecha) = '2025-04'
#GROUP BY v.fecha
#ORDER BY v.fecha;

# 9. Venta total y unidades por vendedora
#SELECT e.nombre, e.apellido, SUM(dv.cantidad * dv.precio_unitario) AS total_venta, SUM(dv.cantidad) AS unidades
#FROM Empleado e
#JOIN Venta v ON e.id_empleado = v.id_empleado
#JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
#HERE e.rol = 'Vendedora' AND strftime('%Y-%m', v.fecha) = '2025-04'
#GROUP BY e.id_empleado;

# 10. Ticket promedio por vendedora
#SELECT e.nombre, e.apellido, 
#       AVG(t.total) AS ticket_promedio
#FROM Empleado e
#JOIN (
 #   SELECT v.id_empleado, v.id_venta, SUM(dv.cantidad * dv.precio_unitario) AS total
  #  FROM Venta v
   # JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
    #WHERE strftime('%Y-%m', v.fecha) = '2025-04'
    #GROUP BY v.id_venta
#) t ON e.id_empleado = t.id_empleado
#WHERE e.rol = 'Vendedora'
#GROUP BY e.id_empleado;

#-- 11. Stock negativo en locales
#SELECT s.nombre AS sucursal, sl.sku_producto, sl.talle_id, sl.cantidad
#FROM Stock_Local sl
#JOIN Sucursal s ON sl.id_sucursal = s.id_sucursal
#WHERE sl.cantidad < 0;

#-- 12. Total vendido por sucursal
#SELECT s.nombre, SUM(dv.cantidad * dv.precio_unitario) AS total
#FROM Venta v
#JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
#JOIN Sucursal s ON v.id_sucursal = s.id_sucursal
#WHERE strftime('%Y-%m', v.fecha) = '2025-04'
#GROUP BY s.id_sucursal;

#-- 13. Cantidad de ventas por empleada
#SELECT e.nombre, e.apellido, COUNT(v.id_venta) AS cantidad_ventas
#FROM Empleado e
#JOIN Venta v ON e.id_empleado = v.id_empleado
#WHERE strftime('%Y-%m', v.fecha) = '2025-04'
#GROUP BY e.id_empleado;

#-- 14. Stock disponible por producto y sucursal
#SELECT s.nombre AS sucursal, p.nombre AS producto, t.descripcion AS talle, sl.cantidad
#FROM Stock_Local sl
#JOIN Producto p ON p.sku = sl.sku_producto
#JOIN Talle t ON t.id_talle = sl.talle_id
#JOIN Sucursal s ON s.id_sucursal = sl.id_sucursal;

#-- 15. Horas extra pagadas en abril por empleada
#SELECT e.nombre, e.apellido, pe.horas_extra
#FROM Empleado e
#JOIN Pago_Empleado pe ON e.id_empleado = pe.id_empleado
#WHERE pe.mes = 4 AND pe.anio = 2025;

#-- 16. Pagos totales por empleada en abril
#SELECT e.nombre, e.apellido, pe.total_pago
#FROM Empleado e
#JOIN Pago_Empleado pe ON e.id_empleado = pe.id_empleado
#WHERE pe.mes = 4 AND pe.anio = 2025;

#-- 17. Promedio de ticket por sucursal
#SELECT s.nombre, 
#       AVG(total) AS ticket_promedio
#FROM (
#  SELECT v.id_sucursal, v.id_venta, SUM(dv.cantidad * dv.precio_unitario) AS total
#  FROM Venta v
#  JOIN Detalle_Venta dv ON v.id_venta = dv.id_venta
#  WHERE strftime('%Y-%m', v.fecha) = '2025-04'
#  GROUP BY v.id_venta
#) t
#JOIN Sucursal s ON s.id_sucursal = t.id_sucursal
#GROUP BY s.nombre;

#-- 18. Detalle de pagos de empleados con desglose
#SELECT e.nombre, e.apellido, e.rol, e.sueldo_basico, 
#       pe.comision, pe.horas_extra, pe.total_pago
#FROM Empleado e
#JOIN Pago_Empleado pe ON e.id_empleado = pe.id_empleado
#WHERE pe.mes = 4 AND pe.anio = 2025;

#-- 19. Productos sin ventas
#SELECT p.nombre
#FROM Producto p
#LEFT JOIN Detalle_Venta dv ON p.sku = dv.sku
#WHERE dv.id_venta IS NULL;

#-- 20. Clientes que compraron más de una vez
#SELECT c.nombre_completo, COUNT(v.id_venta) AS veces
#FROM Cliente c
#JOIN Venta v ON c.id_cliente = v.id_cliente
#GROUP BY c.id_cliente
#HAVING veces > 1;

# 21. Clientes sin mail (placeholder)
#SELECT *
#FROM Cliente
#WHERE mail LIKE 'Cliente%';
