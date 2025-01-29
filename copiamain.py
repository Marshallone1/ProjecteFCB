import os
import sqlite3
#from src.databaseSetup import setup_database
from src.classifyPDF import classify_pdfs
from tests.generate_fake_demand import generate_fake_demand
from src.convertPDF import convert_pdf_L2425
from src.config import OUTPUT_DIR, CLASSIFIED_DIR

# Función para obtener datos de demanda no procesados desde la base de datos
def get_unprocessed_demand_data():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id, date, boca, fila, asiento, name, dni FROM demanda WHERE processed = 0')
    demand_data = cursor.fetchall()
    conn.close()
    return demand_data

# Función para marcar una entrada de demanda como procesada
def mark_demand_as_processed(demand_id, date, boca, fila, asiento):
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()
    cursor.execute('UPDATE demanda SET processed = 1 WHERE id = ?', (demand_id,))
    cursor.execute('UPDATE oferta SET processed = 1 WHERE date = ? AND boca = ? AND fila = ? AND asiento = ?', (date, boca, fila, asiento))
    conn.commit()
    conn.close()

# Función para procesar y renombrar las entradas
def process_and_rename_entries():
    demand_data = get_unprocessed_demand_data()

    for date_folder in os.listdir(CLASSIFIED_DIR):
        classified_date_dir = os.path.join(CLASSIFIED_DIR, date_folder)
        if os.path.isdir(classified_date_dir):
            for page_filename in os.listdir(classified_date_dir):
                if page_filename.endswith(".pdf"):
                    input_page_pdf = os.path.join(classified_date_dir, page_filename)

                    # Obtener el nombre y DNI del comprador correspondiente
                    if demand_data:
                        demand_id, date, boca, fila, asiento, name, dni = demand_data.pop(0)
                        replacements = [f"{name} "] #DNI:{dni} se puede añadir si se quiere
                        # Reemplazar '/' en la fecha por '-'
                        safe_date = date.replace("/", "-")
                        output_pdf = os.path.join(OUTPUT_DIR, f"{safe_date}_{boca}_{fila}_{asiento}.pdf")
                        print(f"Procesando: {input_page_pdf} -> {output_pdf}")
                        convert_pdf_L2425(input_page_pdf, output_pdf, replacements)
                        print(f"Entrada procesada y renombrada: {output_pdf}")
                        if os.path.exists(output_pdf):
                            print(f"Archivo guardado correctamente: {output_pdf}")
                            # Marcar la entrada de demanda y oferta como procesada
                            mark_demand_as_processed(demand_id, date, boca, fila, asiento)
                        else:
                            print(f"Error al guardar el archivo: {output_pdf}")

if __name__ == "__main__":
    # Verificar si existe la base de datos y crearla si no existe
    #setup_database()

    # Actualizar la base de datos con las nuevas entradas usando classifyPDF.py
    classify_pdfs()

    # Generar datos de demanda falsos y actualizar la base de datos de demanda
    generate_fake_demand()

    # Ligar los datos de oferta y demanda y transformar los PDFs que se puedan convertir
    process_and_rename_entries()

    print("Proceso completado.")