import os
import fitz  # PyMuPDF
from datetime import datetime  # Importar datetime
from config import PDF_DIR_COMPRA, PDF_DIR_PASSI, PDF_DIR_COMPRA2  # Importar rutas de directorios
from lecturaPDF import extract_ticket_data, extract_ticket_data_v2

def test_extract_data():
    # Procesar la primera página del primer archivo PDF en PDF_DIR_PASSI
    passi_files = [f for f in os.listdir(PDF_DIR_PASSI) if f.endswith(".pdf")]
    if passi_files:
        pdf_path = os.path.join(PDF_DIR_PASSI, passi_files[0])
        doc = fitz.open(pdf_path)
        single_page_doc = fitz.open()  # Crear un nuevo documento PDF
        single_page_doc.insert_pdf(doc, from_page=0, to_page=0)
        single_page_path = os.path.join(PDF_DIR_PASSI, "temp_page.pdf")
        single_page_doc.save(single_page_path)
        single_page_doc.close()
        ticket_info = extract_ticket_data(single_page_path)
        os.remove(single_page_path)  # Eliminar el archivo temporal
        print(f"Datos extraídos de la primera página del primer PDF en PDF_DIR_PASSI ({passi_files[0]}):")
        print(ticket_info)
    else:
        print("No se encontraron archivos PDF en PDF_DIR_PASSI.")

    # Procesar la primera página del primer archivo PDF en PDF_DIR_COMPRA
    compra_files = [f for f in os.listdir(PDF_DIR_COMPRA) if f.endswith(".pdf")]
    if compra_files:
        pdf_path = os.path.join(PDF_DIR_COMPRA, compra_files[0])
        doc = fitz.open(pdf_path)
        single_page_doc = fitz.open()  # Crear un nuevo documento PDF
        single_page_doc.insert_pdf(doc, from_page=0, to_page=0)
        single_page_path = os.path.join(PDF_DIR_COMPRA, "temp_page.pdf")
        single_page_doc.save(single_page_path)
        single_page_doc.close()
        ticket_info = extract_ticket_data_v2_with_debug(single_page_path)
        os.remove(single_page_path)  # Eliminar el archivo temporal
        print(f"Datos extraídos de la primera página del primer PDF en PDF_DIR_COMPRA ({compra_files[0]}):")
        print(ticket_info)
    else:
        print("No se encontraron archivos PDF en PDF_DIR_COMPRA.")

    # Procesar la primera página del primer archivo PDF en PDF_DIR_COMPRA2
    compra2_files = [f for f in os.listdir(PDF_DIR_COMPRA2) if f.endswith(".pdf")]
    if compra2_files:
        pdf_path = os.path.join(PDF_DIR_COMPRA2, compra2_files[0])
        doc = fitz.open(pdf_path)
        single_page_doc = fitz.open()  # Crear un nuevo documento PDF
        single_page_doc.insert_pdf(doc, from_page=0, to_page=0)
        single_page_path = os.path.join(PDF_DIR_COMPRA2, "temp_page.pdf")
        single_page_doc.save(single_page_path)
        single_page_doc.close()
        ticket_info = extract_ticket_data_v3(single_page_path)
        os.remove(single_page_path)  # Eliminar el archivo temporal
        print(f"Datos extraídos de la primera página del primer PDF en PDF_DIR_COMPRA2 ({compra2_files[0]}):")
        print(ticket_info)
    else:
        print("No se encontraron archivos PDF en PDF_DIR_COMPRA2.")

def extract_ticket_data_v2_with_debug(pdf_path):
    ticket_data = None
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        text = page.get_text("text")
        lines = text.split('\n')

        # Encontrar el índice de la línea que comienza con "FC BARCELONA -"
        start_index = next(i for i, line in enumerate(lines) if line.startswith("FC BARCELONA -"))

        # Añadir depuración para ver las líneas extraídas
        for i in range(start_index, start_index + 15):
            print(f"Línea {i - start_index}: {lines[i]}")

        # Extraer la información relevante
        date_str = lines[start_index + 4].strip()  # Ajustar el índice para la fecha
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        date_int = int(date_obj.strftime("%Y%m%d"))

        boca_str = lines[start_index + 7].strip()
        boca = int(boca_str) if boca_str.isdigit() else None

        fila = lines[start_index + 8].strip()
        asiento = lines[start_index + 9].strip()

        # Crear el diccionario con la información extraída
        ticket_data = {
            "date": date_int,
            "boca": boca,
            "fila": fila,
            "asiento": asiento
        }

    except (IndexError, ValueError, StopIteration) as e:
        print(f"Error al extraer datos del PDF: {e}")
    
    return ticket_data

def extract_ticket_data_v3(pdf_path):
    ticket_data = None
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        text = page.get_text("text")
        lines = text.split('\n')

        # Encontrar el índice de la línea que comienza con "FC BARCELONA -"
        start_index = next(i for i, line in enumerate(lines) if line.startswith("FC BARCELONA -"))

        # Extraer la información relevante
        date_str = lines[start_index + 4].strip()  # Ajustar el índice para la fecha
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
        print(f"Error al extraer datos del PDF: {e}")
    
    return ticket_data

if __name__ == "__main__":
    test_extract_data()