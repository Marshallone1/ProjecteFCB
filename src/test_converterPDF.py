import os
import sys
import fitz  # PyMuPDF

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from convertPDF import convert_pdf_L2425
from config import INPUT_DIR, OUTPUT_DIR

def test_replace_text_in_single_page_pdf():
    input_pdf = os.path.join(INPUT_DIR, 'C:/Users/Inorbis/ProjecteFCB/data/EntradasPrueba/Urioste.pdf')
    output_pdf = os.path.join('C:/Users/Inorbis/ProjecteFCB/data/EntradasPrueba/', 'UriosteDNI.pdf')
    replacement_texts = ["JAVIER URIOSTE TORNE DNI:78578615N"]

    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(input_pdf):
        raise FileNotFoundError(f"El archivo de entrada {input_pdf} no existe.")

    convert_pdf_L2425(input_pdf, output_pdf, replacement_texts)

    doc = fitz.open(output_pdf)
    page = doc[0]
    text = page.get_text("text")
    doc.close()

    print("Texto extraído del PDF después de la conversión:")
    print(text)

    assert any(replacement_text in text for replacement_text in replacement_texts), "El texto no fue reemplazado correctamente"

if __name__ == "__main__":
    test_replace_text_in_single_page_pdf()