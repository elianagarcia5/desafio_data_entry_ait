Tarea 2: Implementar las sentencias SQL para los ítems a continuación:

a. Obtener todos los Repuestos del Proveedor Autofix cuyo precio no se haya actualizado en el último mes.
SELECT r.*
FROM Repuesto r
JOIN Proveedor p ON r.proveedor_id = p.id
LEFT JOIN Actualizacion a ON r.id_ultima_actualizacion = a.id
WHERE p.nombre = 'Autofix'
  AND (a.fecha IS NULL OR a.fecha < NOW() - INTERVAL 1 MONTH);



b. Actualizar los Repuestos de las Marcas “ELEXA”, “BERU”, “SH”, “MASTERFILT” y “RN” realizando un incremento del 15% en sus precios.
UPDATE Repuesto r
JOIN Marca m ON r.id_marca = m.id
SET r.precio = r.precio * 1.15
WHERE m.nombre IN ('ELEXA', 'BERU', 'SH', 'MASTERFILT', 'RN');


c. Obtener el promedio de precios de los repuestos por cada marca.
SELECT m.nombre AS Marca, AVG(r.precio) AS PromedioPrecio
FROM Repuesto r
JOIN Marca m ON r.id_marca = m.id
GROUP BY m.nombre;


d. Obtener los repuestos que no tienen una descripción asignada (descripción es NULL o vacía).
SELECT *
FROM Repuesto
WHERE descripcion IS NULL OR descripcion = '';


e. Contar el número de repuestos de cada proveedor y mostrar sólo aquellos proveedores que tienen al menos 1000 repuestos.
SELECT p.nombre AS Proveedor, COUNT(r.id) AS CantidadRepuestos
FROM Repuesto r
JOIN Proveedor p ON r.proveedor_id = p.id
GROUP BY p.nombre
HAVING COUNT(r.id) >= 1000;



f. Obtener el repuesto más caro de cada proveedor.
SELECT p.nombre AS Proveedor, r.*
FROM Repuesto r
JOIN Proveedor p ON r.proveedor_id = p.id
WHERE r.precio = (
    SELECT MAX(r2.precio)
    FROM Repuesto r2
    WHERE r2.proveedor_id = p.id
);


g. Aplicar un recargo del 30% en los artículos de los proveedores AutoRepuestos Express y Automax cuyo precio sea mayor a $50000 y menor a $100000.
UPDATE Repuesto r
JOIN Proveedor p ON r.proveedor_id = p.id
SET r.precio = r.precio * 1.30
WHERE p.nombre IN ('AutoRepuestos Express', 'Automax')
  AND r.precio > 50000
  AND r.precio < 100000;