CREATE TABLE IF NOT EXISTS {table_name} (
	Pedido SMALLINT,
	Producto VARCHAR(100),
	Cantidad SMALLINT,
	Precio	NUMERIC,
	Descuento VARCHAR(50),
	Antes_del_descuento	NUMERIC,
	Tarifa_de_servicio	NUMERIC,
	Total_del_pago NUMERIC,
	Tipo_de_pago VARCHAR(50),
	Genero VARCHAR(20),
	Fecha DATE,
	Momento_del_dia	VARCHAR(20),
	Dia_de_la_semana VARCHAR(20),
	Canal_de_venta VARCHAR(20)
);