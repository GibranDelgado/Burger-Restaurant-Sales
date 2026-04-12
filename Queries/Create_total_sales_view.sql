CREATE OR REPLACE VIEW {view_name} AS 
SELECT
	Pedido,
	Producto,
	Cantidad,
	Precio,
	Descuento,
	Antes_del_descuento,
	Tarifa_de_servicio,
	Total_del_pago,
	Tipo_de_pago,
	NULL AS Edad_del_consumidor,
	Genero,
	Fecha,
	Momento_del_dia,
	Dia_de_la_semana,
	Canal_de_venta
FROM digitalsales
UNION ALL
SELECT
	NULL AS Pedido,
	Producto,
	Cantidad,
	Precio,
	Descuento,
	NULL AS Antes_del_descuento,
	NULL AS Tarifa_de_servicio,
	Total_del_pago,
	Tipo_de_pago,
	Edad_del_consumidor,
	Genero,
	Fecha,
	Momento_del_dia	,
	Dia_de_la_semana,
	Canal_de_venta 
FROM storesales;