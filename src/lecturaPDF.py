import fitz  # PyMuPDF
import re
import sqlite3
import os
from datetime import datetime
from config import PDF_DIR_PASSI, PDF_DIR_COMPRA, OUTPUT_DIR, DB_PATH, UNPROCESSED_DIR

def validate_data(data):
    errors = []

    # Validar fecha (YYYYMMDD)
    if not re.match(r"^\d{8}$", str(data["date"])):
        errors.append("Fecha inválida")

    # Validar boca (número entero)
    if not isinstance(data["boca"], int):
        errors.append("Boca debe ser un número entero")

    # Validar fila (cadena no vacía)
    if not data["fila"]:
        errors.append("Fila no puede estar vacía")

    # Validar asiento (cadena no vacía)
    if not data["asiento"]:
        errors.append("Asiento no puede estar vacío")

    return errors

# Función para extraer datos del ticket a partir de la línea que comienza con "FC BARCELONA -"
def extract_ticket_data(pdf_path):
    doc = fitz.open(pdf_path)
    ticket_data = []

    # Leer solo la primera página del documento
    text = doc[0].get_text()

    try:
        lines = text.splitlines()

        # Buscar inicio de datos relevantes
        start_index = next(i for i, line in enumerate(lines) if line.startswith("FC BARCELONA -"))
        relevant_lines = lines[start_index:]

        # Extraer fecha de la línea siguiente al título
        date_time = relevant_lines[1]
        date = date_time.split()[0]
        
        date_str = date.split()[0]
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        date_int = int(date_obj.strftime("%Y%m%d"))

        # Extraer boca, fila y asiento desde las líneas relevantes
        boca = int(relevant_lines[6].strip())
        fila = relevant_lines[7].strip()
        asiento = relevant_lines[8].strip()

        ticket_data.append({
            "date": date_int,
            "boca": boca,
            "fila": fila,
            "asiento": asiento
        })

    except (IndexError, ValueError, StopIteration) as e:
        pass
    finally:
        doc.close()

    return ticket_data[0] if ticket_data else None

# v2 entradas compra, funcion para extraer datos del ticket a partir de la línea que comienza con "FC BARCELONA -"
def extract_ticket_data_v2(pdf_path):
    ticket_data = None
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        text = page.get_text("text")
        lines = text.split('\n')

        # Encontrar el índice de la línea que comienza con "FC BARCELONA -"
        start_index = next(i for i, line in enumerate(lines) if line.startswith("FC BARCELONA -"))

        # Extraer la información relevante
        date_str = lines[start_index + 4].strip()
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        date_int = int(date_obj.strftime("%Y%m%d"))

        boca_str = lines[start_index + 8].strip()
        boca = int(boca_str) if boca_str.isdigit() else None
        fila_asiento = lines[start_index + 9].strip().split()
        fila = fila_asiento[0]
        asiento = fila_asiento[1]

        # Crear el diccionario con la información extraída
        ticket_data = {
            "date": date_int,
            "boca": boca,
            "fila": fila,
            "asiento": asiento
        }

    except (IndexError, ValueError, StopIteration) as e:
        pass
    
    return ticket_data

# Función para guardar datos en la base de datos de oferta sin duplicados
def save_to_database(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Verificar si la entrada ya existe en la base de datos
    cursor.execute('''
        SELECT COUNT(*) FROM oferta WHERE date = ? AND boca = ? AND fila = ? AND asiento = ?
    ''', (data["date"], data["boca"], data["fila"], data["asiento"]))
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO oferta (date, boca, fila, asiento)
            VALUES (?, ?, ?, ?)
        ''', (data["date"], data["boca"], data["fila"], data["asiento"]))
        conn.commit()
    conn.close()

# Función para mover archivos a la carpeta UNPROCESSED_DIR con un nombre único
def move_to_unprocessed(file_path):
    base_name = os.path.basename(file_path)
    unprocessed_path = os.path.join(UNPROCESSED_DIR, base_name)
    counter = 1
    while os.path.exists(unprocessed_path):
        name, ext = os.path.splitext(base_name)
        unprocessed_path = os.path.join(UNPROCESSED_DIR, f"{name}_{counter}{ext}")
        counter += 1
    os.rename(file_path, unprocessed_path)

# Función para procesar PDFs y añadir datos a la base de datos de oferta
def process_pdf(file_path, extract_function):
    doc = fitz.open(file_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        single_page_doc = fitz.open()  # Crear un nuevo documento PDF
        single_page_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        single_page_path = os.path.join(OUTPUT_DIR, f"page_{page_num + 1}.pdf")
        single_page_doc.save(single_page_path)
        single_page_doc.close()

        ticket_info = extract_function(single_page_path)
        if ticket_info:
            errors = validate_data(ticket_info)
            if errors:
                move_to_unprocessed(single_page_path)
            else:
                try:
                    save_to_database(ticket_info)
                    # Renombrar el archivo con la información del ticket
                    new_filename = f"{ticket_info['date']}_{ticket_info['boca']}_{ticket_info['fila']}_{ticket_info['asiento']}.pdf"
                    os.rename(single_page_path, os.path.join(OUTPUT_DIR, new_filename))
                except Exception:
                    move_to_unprocessed(single_page_path)
        else:
            move_to_unprocessed(single_page_path)

# Función principal para procesar todas las entradas
def process_all_pdfs():
    # Procesar los archivos PDF en PDF_DIR_PASSI
    for filename in os.listdir(PDF_DIR_PASSI):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR_PASSI, filename)
            process_pdf(pdf_path, extract_ticket_data)

    # Procesar los archivos PDF en PDF_DIR_COMPRA
    for filename in os.listdir(PDF_DIR_COMPRA):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR_COMPRA, filename)
            process_pdf(pdf_path, extract_ticket_data_v2)

if __name__ == "__main__":
    process_all_pdfs()