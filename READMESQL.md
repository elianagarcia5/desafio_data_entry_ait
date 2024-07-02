#### Sentencias para actualizar database SQL, se agregaron al final del sql_scripts del desafio

1. -- Obtener todos los Repuestos del Proveedor Autofix no actualizado en el último mes
SELECT *
FROM actualizacion
WHERE proveedor_id = '4'
AND fecha < DATE_SUB(NOW(), INTERVAL 1 MONTH);

2. -- Actualizar los repuesto de las Marcas “ELEXA”, “BERU”, “SH”, “MASTERFILT” y “RN” un 15% en sus precios
UPDATE repuesto
SET precio = precio * 1.15
WHERE marca_id IN ('286', '264', '211', '95', '68');

3. -- Obtener el promedio de precios de repuesto por marca
SELECT marca_id, AVG(precio) AS promedio_precio
FROM repuesto
GROUP BY marca_id;

4. -- Obtener los repuesto que no tienen una descripción asignada
SELECT *
FROM repuesto
WHERE descripcion IS NULL OR descripcion = '';

5. -- Contar el número de repuesto de cada proveedor y mostrar sólo aquellos proveedores que tienen al menos 1000 repuesto
SELECT proveedor_id, COUNT(*) AS total_repuesto
FROM repuesto
GROUP BY proveedor_id
HAVING COUNT(*) >= 1000;

6. -- Obtener el repuesto más caro de cada proveedor
SELECT proveedor_id, MAX(precio) AS precio_mas_caro
FROM repuesto
GROUP BY proveedor_id;

7. -- Aplicar un recargo del 30% en los proveedores Autorepuesto Express y Automax con el precio mayor a $50000 y menor a $100000
UPDATE repuesto
SET precio = precio * 1.30
WHERE proveedor_id IN ('9', '6')
AND precio > 50000
AND precio < 100000;