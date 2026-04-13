# Pipeline ETL de ventas
Este proyecto tiene como finalidad automatizar la extracción, limpieza y carga (ETL) de datos de ventas provenientes de diferentes fuentes de Google Sheets hacia una base de datos centralizada en PostgreSQL. 
El objetivo principal es normalizar la información de ventas físicas y digitales para facilitar su análisis y visualización a través de Power BI.

## ⚙️ Arquitectura del proyecto
1. **Extracción**: Conexión a múltiples hojas de cálculo (ventas semanales en tienda e histórico digital) mediante la API de Google Sheets utilizando un Service Account en Google Cloud Platform (GCP).
2. **Transformación**: Procesamiento de datos con Pandas.
   - Limpieza de columnas y normalización de nombres.
   - Conversión de tipos de datos (fechas, monedas, enteros).
   - Manejo de valores nulos y filtrado de productos excluidos.
   - Enriquecimiento de datos (cálculo de días de la semana, asignación de canales de venta).
3. **Carga**: Inserción de los dataframes en PostgreSQL mediante psycopg2 y creación de una vista unificada para análisis global.

## 📊 Dashboard
![image alt](https://github.com/GibranDelgado/Burger-Restaurant-Sales/blob/master/sales.jpg?raw=true)

## 🗂️ Estructura del repositorio

### 📁 Scripts

#### 🚀 main_workflow
Punto de entrada que coordina la ejecución de todo el pipeline.

#### 🔑 google_sheets_client
Manejo de autenticación y conexión con GCP.

#### 🧹sales_data_processing
Lógica de negocio y métodos de limpieza de datos.

#### 🏗️ total_sales_pipeline
Orquestador intermedio para la obtención de los dataframes de las ventas físicas y digitales.

#### 🚚 postgres_pipeline
Gestión de conexiones a BD, creación de esquemas e inserción masiva de datos.

### 📁 Queries
Archivos .sql para la definición de tablas y de la vista consolidada.

### 📁 Input_files
Directorio (ignorado en git) para alojar .env y credentials.json.

## 🚀 Requisitos e instalación
**1. Clonar el repositorio:**

`git clone https://github.com/tu-usuario/nombre-repo.git`

**2. Instalar dependencias:**

`pip install pandas gspread google-auth google-api-python-client psycopg2 python-dotenv`

**3. Configuración de Credenciales:**
   - Crea un proyecto en Google Cloud Console.
   - Habilita Google Sheets y Google Drive API.
   - Genera una Service Account Key en formato JSON y guárdala como credentials_HH.json en la carpeta `Input_files`.
   - Configura un archivo .env con las siguientes variables: `db_name`, `user`, `password`

## 🛠️ Uso
Para ejecutar el pipeline completo y actualizar tu base de datos, simplemente corre el script:
`python main_workflow.py`

## 📊 Visualización (Power BI)
Esta etapa final transforma los datos normalizados en una herramienta de toma de decisiones. Al tener conectada la vista totalsales de PostgreSQL con Power BI, nos aseguramos de no depender de archivos planos como fuentes de datos, además de poder tener la información actualizada en todo momento, simplemente ejecutando el archivo main_workflow de python.

### 📈 KPIs:
- **Venta total:** Consolidado global de ingresos (tienda + digital).
- **Venta promedio diaria:** Métrica para medir la consistencia de ingresos y establecer metas.
- **Volumen de pedidos:** Promedio diario de pedidos digitales
- **Impacto de promociones:** Análisis comparativo de ventas con y sin descuentos aplicados, permitiendo evaluar la efectividad de las campañas.

### Comportamiento del Consumidor:
- **Perfil Demográfico:** Distribución de ventas por `Genero` y `Edad del consumidor` (datos exclusivos de ventas en tienda).
- **Hábitos de Compra:** Identificación de los `Momento del dia` con mayor flujo y los productos estrella por cada franja horaria.

### Eficacia operativa:
- Análisis temporal por `Dia de la semana` para optimizar el stock y personal según la demanda histórica.
- Seguimiento de métodos de pago (`Tipo de pago`) para entender la preferencia de los usuarios en cada canal.

### Desglose de productos y operación diaria
Para optimizar el inventario y la producción, el informe detalla el volumen de productos diarios vendidos. Esto permite saber con precisión:
- **Proteínas y principales:** Cantidad diaria de carnes para hamburguesa y burritos preparados.
- **Complementos y bebidas:** Volumen de órdenes de papas fritas y malteadas.
- **Insumos base:** Control de salida de bolsas de pan y otros productos esenciales.


