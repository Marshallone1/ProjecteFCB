import fitz  # PyMuPDF
import os

def print_pdf_text(file_path):
    # Abrir el archivo PDF
    doc = fitz.open(file_path)
    # Obtener la primera página
    page = doc[0]
    # Obtener el texto de la página
    text = page.get_text("text")
    # Imprimir el texto
    print(text)

if __name__ == "__main__":
    # Ruta del archivo PDF de entrada
    input_pdf = "C:/Users/Inorbis/ProjecteFCB/data/input/LecturaEntradasCompra/128.17.20-22-24.pdf"
    
    if os.path.exists(input_pdf):
        print_pdf_text(input_pdf)
    else:
        print(f"El archivo {input_pdf} no existe.")