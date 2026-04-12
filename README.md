# Pipeline ETL de ventas
Este proyecto automatiza la extracción, limpieza y carga (ETL) de datos de ventas provenientes de diferentes fuentes de Google Sheets hacia una base de datos centralizada en PostgreSQL. 
El objetivo principal es normalizar la información de ventas físicas y digitales para facilitar su análisis y visualización a través de Power BI.

## ⚙️ Arquitectura del proyecto
1. Extracción: Conexión a múltiples hojas de cálculo (ventas semanales en tienda e histórico digital) mediante la API de Google Sheets utilizando un Service Account en GCP.
2. Transformación: Procesamiento de datos con Pandas.
   - Limpieza de columnas y normalización de nombres.
   - Conversión de tipos de datos (fechas, monedas, enteros).
   - Manejo de valores nulos y filtrado de productos excluidos.
   - Enriquecimiento de datos (cálculo de días de la semana, asignación de canales de venta).
3. Carga: Inserción de los dataframes en PostgreSQL mediante psycopg2 y creación de una vista unificada (UNION ALL) para análisis global.

## 📂 Estructura del repositorio
- main_workflow.py: Punto de entrada que coordina la ejecución de todo el pipeline.
- `Scripts/`:
  - `google_sheets_client.py`: Manejo de autenticación y conexión con Google Cloud Platform.
  - `sales_data_processing.py`: Lógica de negocio y métodos de limpieza de datos.
  - `total_sales_pipeline.py`: Orquestador intermedio para la obtención de dataframes procesados.
  - `postgres_pipeline.py`: Gestión de conexiones a BD, creación de esquemas e inserción masiva de datos.

- `Queries/`: Archivos .sql para la definición de tablas y la vista consolidada.
- `Input_files/`: Directorio (ignorado en git) para alojar .env y credentials.json.

## 🚀 Requisitos e instalación
1. Clonar el repositorio:

`git clone https://github.com/tu-usuario/nombre-repo.git`

2. Instalar dependencias:

`pip install pandas gspread google-auth google-api-python-client psycopg2 python-dotenv`

3. Configuración de Credenciales:
   - Crea un proyecto en Google Cloud Console.
   - Habilita Google Sheets y Google Drive API.
   - Genera una Service Account Key en formato JSON y guárdala como credentials_HH.json en Input_files/.
   - Configura un archivo .env con las siguientes variables: `db_name`, `user`, `password`

## 🛠️ Uso
Para ejecutar el pipeline completo y actualizar tu base de datos, simplemente corre el script:
`python main_workflow.py`

## 📊 Visualización (Power BI)
Una vez que el script finaliza, la base de datos PostgreSQL contendrá la vista `totalsales`. Conecta Power BI a esta tabla para diseñar el dashboard de ventas
