import os
import fitz  # PyMuPDF
from src.config import PDF_DIR_COMPRA, PDF_DIR_PASSI
from src.lecturaPDF import extract_ticket_data, extract_ticket_data_v2

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
        ticket_info = extract_ticket_data_v2(single_page_path)
        os.remove(single_page_path)  # Eliminar el archivo temporal
        print(f"Datos extraídos de la primera página del primer PDF en PDF_DIR_COMPRA ({compra_files[0]}):")
        print(ticket_info)
    else:
        print("No se encontraron archivos PDF en PDF_DIR_COMPRA.")

if __name__ == "__main__":
    test_extract_data()