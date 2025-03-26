import os
import fitz  # PyMuPDF
import sqlite3
from config import OUTPUT_AS_DIR, OUTPUT_PEDIDO_DIR, DB_PATH

def extract_info_from_filename(filename):
    parts = filename.split('_')
    if len(parts) >= 5:
        pedido_id = parts[0]
        # fecha = parts[1]
        boca = parts[2]
        fila = parts[3]
        asiento = parts[4].split('.')[0]
        return pedido_id, boca, fila, asiento
    return None, None, None, None, None

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
        
        # Extraer información de boca, fila y asiento de los nombres de los archivos PDF
        pdf_files_info = []
        for pdf_file in pdf_files:
            _, boca, fila, asiento = extract_info_from_filename(pdf_file)
            if boca and fila and asiento:
                pdf_files_info.append((boca, fila, asiento, pdf_file))
        
        # Ordenar los archivos PDF por boca, fila y asiento
        pdf_files_info.sort(key=lambda x: (int(x[0]), int(x[1]), int(x[2])))
        
        for _, _, _, pdf_file in pdf_files_info:
            input_pdf_path = os.path.join(OUTPUT_AS_DIR, pdf_file)
            input_pdf = fitz.open(input_pdf_path)
            output_pdf.insert_pdf(input_pdf)
            input_pdf.close()
        
        # Guardar el PDF empaquetado solo si contiene páginas
        if len(output_pdf) > 0:
            output_pdf.save(output_pdf_path)
            print(f"Pedido {pedido_id} guardado exitosamente en {output_pdf_path}")
        else:
            print(f"No se encontraron archivos PDF para el pedido {pedido_id}")
        
        output_pdf.close()
    
    conn.close()

if __name__ == "__main__":
    package_pdfs()
    print("Empaquetado de PDFs completado exitosamente.")