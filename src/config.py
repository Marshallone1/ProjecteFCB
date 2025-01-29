import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSIFIED_DIR = os.path.join(BASE_DIR, 'data', 'classified')
UNPROCESSED_DIR = os.path.join(BASE_DIR, 'unprocessed')

# Rutas
FONT_PATH = os.path.join(BASE_DIR, 'data', 'fonts', 'font-0025.ttf')
INPUT_DIR = os.path.join(BASE_DIR, 'data', 'input')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'output')

# Input
PDF_DIR_PASSI = os.path.join(INPUT_DIR, 'LecturaEntradasPassi')
PDF_DIR_COMPRA = os.path.join(INPUT_DIR, 'LecturaEntradasCompra')
CLASSIFIED_DIR = os.path.join(INPUT_DIR, 'EntradesClasificadas')  # Directorio clasificado por partido (fecha)

# Output
OUTPUT_AS_DIR = os.path.join(BASE_DIR, 'data', 'outputAS')
OUTPUT_PEDIDO_DIR = os.path.join(BASE_DIR, 'data', 'outputPEDIDO')

# Base de datos
DB_PATH = os.path.join(BASE_DIR, 'tickets.db')

# Parámetros
FONT_SIZE = 8.64
Y_CORRECTION_FACTOR = 3
CUSTOM_FONT_NAME = "FC_BARCELONA"

# Configuración del servidor de correo
imap_server = "imap.gmail.com"
email_user = "registros.ventas.completadas@gmail.com"
email_pass = "lghe mzod iqed yfzw"  # Asegúrate de usar una contraseña de aplicación si usas Gmail

# Ruta al archivo CSV
csv_filepath = os.path.join(INPUT_DIR, 'Asignacion', 'PlantillaBetis.csv')
