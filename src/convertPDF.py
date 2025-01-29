import fitz  # PyMuPDF
import re
from itertools import cycle
from src.config import FONT_PATH, FONT_SIZE, Y_CORRECTION_FACTOR, CUSTOM_FONT_NAME

def convert_pdf_L2425(input_pdf, output_pdf, replacements):
    try:
        doc = fitz.open(input_pdf)
        page = doc[0]
        text = page.get_text("text")
        
        # Ajustar la expresión regular para encontrar nombres y números
        matches = re.findall(r"[A-ZÁÉÍÓÚÑa-záéíóúñ ]+ DNI:\d{8}[A-Z]", text)
        matches += re.findall(r"[A-ZÁÉÍÓÚÑa-záéíóúñ ]+ \d{6}", text)
        
        replacement_cycle = cycle(replacements)

        for match in matches:
            new_text = next(replacement_cycle)
            areas = page.search_for(match)

            for area in areas:
                x0, y0, x1, y1 = area
                middle_y = y0 + (y1 - y0) / 2
                adjusted_y = middle_y + Y_CORRECTION_FACTOR

                # Tapar el texto original con un rectángulo blanco
                page.draw_rect(area, color=(0.8, 0.8, 0.8), fill=(0.8, 0.8, 0.8))

                page.insert_font(fontfile=FONT_PATH, fontname=CUSTOM_FONT_NAME)
                page.insert_text(
                    (x0, adjusted_y),
                    new_text,
                    fontsize=FONT_SIZE,
                    fontname=CUSTOM_FONT_NAME,
                    color=(0, 0, 0),
                )

        doc.save(output_pdf)
    except Exception as e:
        print(f"Error al convertir el PDF: {e}")
    finally:
        if 'doc' in locals():
            doc.close()