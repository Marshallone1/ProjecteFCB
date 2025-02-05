import os
import shutil
from src.config import PDF_DIR, CLASSIFIED_DIR
from src.lecturaPDF import extract_ticket_data, save_to_database

UNPROCESSED_DIR = "unprocessed"

# Función para dividir y clasificar los PDFs por partido (fecha)
def classify_pdfs():
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            input_pdf = os.path.join(PDF_DIR, filename)
            # Dividir el PDF en páginas individuales

            # Clasificar cada página individualmente
            for page_filename in os.listdir(PDF_DIR):
                if page_filename.startswith("page_") and page_filename.endswith(".pdf"):
                    input_page_pdf = os.path.join(PDF_DIR, page_filename)
                    # Obtener la fecha, boca, fila y asiento desde el contenido de la página
                    ticket_info = extract_ticket_data(input_page_pdf)
                    if ticket_info:
                        for info in ticket_info:
                            # Verificar que la información del ticket es válida
                            if 'date' in info and 'boca' in info and 'fila' in info and 'asiento' in info:
                                date = info["date"]
                                boca = info["boca"]
                                fila = info["fila"]
                                asiento = info["asiento"]
                                # Convertir la fecha al formato yyyymmdd
                                safe_date = str(date)
                                classified_dir = os.path.join(CLASSIFIED_DIR, safe_date)
                                if not os.path.exists(classified_dir):
                                    os.makedirs(classified_dir)
                                output_page_pdf = os.path.join(classified_dir, f"{safe_date}_{boca}_{fila}_{asiento}.pdf")
                                # Verificar si el archivo ya existe
                                if not os.path.exists(output_page_pdf):
                                    os.rename(input_page_pdf, output_page_pdf)
                                # Guardar la información del ticket en la base de datos
                                save_to_database(info)
                    else:
                        print(f"No se encontró información relevante en {input_page_pdf}")
                        try:
                            # Intentar mover el archivo a un directorio de no procesados
                            if not os.path.exists(UNPROCESSED_DIR):
                                os.makedirs(UNPROCESSED_DIR)
                            unprocessed_pdf = os.path.join(UNPROCESSED_DIR, os.path.basename(input_page_pdf))
                            shutil.move(input_page_pdf, unprocessed_pdf)
                            print(f"Archivo movido a no procesados: {unprocessed_pdf}")
                        except PermissionError as e:
                            print(f"No se pudo mover {input_page_pdf} debido a un error de permisos: {e}")

if __name__ == "__main__":
    classify_pdfs()