import os
import sqlite3
from src.config import OUTPUT_DIR, OUTPUT_AS_DIR, DB_PATH
from src.databaseSetup import setup_database  # Asegúrate de que esta función esté correctamente importada
from src.convertPDF import convert_pdf_L2425  # Asegúrate de que esta función esté correctamente importada
from src.PedidoPDF import package_pdfs  # Asegúrate de que esta función esté correctamente importada

def match_offers_and_demands():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Seleccionar ofertas y demandas que coincidan y no estén procesadas
    cursor.execute('''
        SELECT o.id, o.date, o.boca, o.fila, o.asiento, d.id, d.name, d.pedido
        FROM oferta o
        JOIN demanda d ON o.date = d.date AND o.boca = d.boca AND o.fila = d.fila AND o.asiento = d.asiento
        WHERE o.processed = 0 AND d.processed = 0 AND d.match_names = 1
    ''')
    
    matches = cursor.fetchall()
    
    for offer_id, date, boca, fila, asiento, demand_id, name, pedido_id in matches:
        # Marcar como procesados
        cursor.execute('UPDATE oferta SET processed = 1 WHERE id = ?', (offer_id,))
        cursor.execute('UPDATE demanda SET processed = 1 WHERE id = ?', (demand_id,))
        
        # Convertir y mover el PDF
        input_pdf = f"{date}_{boca}_{fila}_{asiento}.pdf"
        input_pdf_path = os.path.join(OUTPUT_DIR, input_pdf)
        new_name = f"{pedido_id}_{name}_{date}_{boca}_{fila}_{asiento}.pdf"
        output_pdf = os.path.join(OUTPUT_AS_DIR, new_name)
        replacements = [name]  # Lista de reemplazos, en este caso solo el nombre
        
        if os.path.exists(input_pdf_path):
            convert_pdf_L2425(input_pdf_path, output_pdf, replacements)
        else:
            print(f"Archivo no encontrado: {input_pdf_path}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Verificar y configurar la base de datos
    setup_database()
    
    # Hacer match entre oferta y demanda y convertir PDFs
    match_offers_and_demands()
    
    # Empaquetar los PDFs por pedido
    #package_pdfs()
    
    print("Proceso de conversión y empaquetado de PDFs completado exitosamente.")