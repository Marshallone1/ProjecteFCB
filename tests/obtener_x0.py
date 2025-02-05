import fitz  # PyMuPDF
import re

def obtener_x0(input_pdf):
    try:
        doc = fitz.open(input_pdf)
        page = doc[0]
        text = page.get_text("text")
        
        # Ajustar la expresión regular para encontrar nombres y números
        matches = re.findall(r"[A-ZÁÉÍÓÚÑa-záéíóúñ ]+ DNI:\d{8}[A-Z]", text)
        matches += re.findall(r"[A-ZÁÉÍÓÚÑa-záéíóúñ ]+ \d{6}", text)

        for match in matches:
            areas = page.search_for(match)

            for area in areas:
                x0, y0, x1, y1 = area
                print(f"x0 detectado: {x0}")
                return

    except Exception as e:
        print(f"Error al obtener x0: {e}")
    finally:
        if 'doc' in locals():
            doc.close()

def main():
    input_pdf = "C:/Users/Inorbis/ProjecteFCB/data/EntradasPrueba/Pruebaok.pdf"
    obtener_x0(input_pdf)

if __name__ == "__main__":
    main()