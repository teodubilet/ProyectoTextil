# Proyecto de Análisis de Ventas - Empresa Textil

Este es un **proyecto integrador de análisis de datos** desarrollado para incluir en un portfolio profesional. Simula el proceso completo de construcción de una solución de Business Intelligence para una empresa del rubro **textil**, con múltiples sucursales de venta minorista.

---

## Tecnologías utilizadas

- **SQLite**: para la construcción de la base de datos relacional, creación de tablas, carga de datos inicial y consultas SQL.
- **Python**: utilizado para automatizar procesos sobre la base de datos, como registrar ventas, calcular stock, simular actividad mensual y generar estructuras de pago.
- **Power BI**: para la construcción de dashboards interactivos utilizando medidas DAX, filtros y visualizaciones orientadas a la toma de decisiones.

---

## Bibliotecas de Python utilizadas

- `sqlite3`: conexión directa a la base de datos `.db`.
- `pandas`: manejo de estructuras tipo DataFrame y exportación a Excel.
- `datetime`: generación y control de fechas para simulaciones y registros.

---

## Estructura del proyecto

El proyecto está dividido en las siguientes etapas:

1. **Diseño de base de datos**:  
   Se definieron entidades como Clientes, Productos, Empleados, Ventas, Detalle de ventas, Stock por local, etc.

2. **Carga de datos simulados**:  
   Se simularon productos, empleados, stock y ventas realistas distribuidas a lo largo de un mes completo en dos sucursales: una tradicional y otra en un centro comercial.

3. **Automatización con Python**:  
   Se construyeron funciones para registrar ventas, restar stock, calcular comisiones, identificar clientes frecuentes y más.

4. **Creación de dashboards en Power BI**:
   Se construyeron 3 dashboards principales:
   - **Dashboard local San Isidro**: resumen completo de actividad de una sucursal
   - **Dashboard local Unicenter**: idéntica estructura, para comparación paralela
   - **Dashboard de pagos al personal**: visualización del sueldo final de cada empleada considerando sueldo base, comisiones y horas extra

---

## Objetivos alcanzados

- Simulación realista de un entorno comercial minorista
- Automatización de lógica operativa de ventas
- Visualización clara para análisis de decisiones de negocio
- Aplicación de conceptos de SQL, Python y DAX en un entorno integrado

---

## 📁 Archivos incluidos

- `BBDD Textil.db` → Base de datos relacional SQLite
- `ventas_utils.py` → Funciones principales para registrar ventas
- `simulacion_ventas.py` → Generación automática de ventas del mes
- `pagos_empleados.py` → Cálculo de pagos y comisiones
- `consultas.sql` → Archivo con más de 20 consultas SQL para análisis
- `Dashboards.pbix` → Archivo Power BI con dashboards interactivos
