import os
import fitz  # PyMuPDF
import sqlite3
from src.config import OUTPUT_AS_DIR, OUTPUT_PEDIDO_DIR, DB_PATH

def package_pdfs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener todos los pedidos únicos de la tabla demanda
    cursor.execute('SELECT DISTINCT pedido FROM demanda')
    pedidos = cursor.fetchall()
    
    for pedido in pedidos:
        pedido_id = pedido[0]
        
        # Verificar la cuenta de las entradas que tiene ese pedido en la base de datos demanda
        cursor.execute('SELECT COUNT(*) FROM demanda WHERE pedido = ?', (pedido_id,))
        count = cursor.fetchone()[0]
        
        # Crear un nuevo documento PDF
        output_pdf_path = os.path.join(OUTPUT_PEDIDO_DIR, f"{pedido_id}.pdf")
        output_pdf = fitz.open()
        
        # Buscar los archivos PDF correspondientes en OUTPUT_AS_DIR
        pdf_files = [f for f in os.listdir(OUTPUT_AS_DIR) if f.startswith(f"{pedido_id}_")]
        
        if len(pdf_files) != count:
            print(f"El número de archivos PDF encontrados ({len(pdf_files)}) no coincide con el número de entradas en la base de datos ({count}) para el pedido {pedido_id}")
            continue
        
        for pdf_file in pdf_files:
            input_pdf_path = os.path.join(OUTPUT_AS_DIR, pdf_file)
            input_pdf = fitz.open(input_pdf_path)
            output_pdf.insert_pdf(input_pdf)
            input_pdf.close()
        
        # Guardar el PDF empaquetado solo si contiene páginas
        if len(output_pdf) > 0:
            output_pdf.save(output_pdf_path)
        else:
            print(f"No se encontraron archivos PDF para el pedido {pedido_id}")
        
        output_pdf.close()
    
    conn.close()

if __name__ == "__main__":
    package_pdfs()
    print("Empaquetado de PDFs completado exitosamente.")