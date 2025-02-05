import os
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from config import DB_PATH, OUTPUT_PEDIDO_DIR

def generar_reporte_partido(fecha_partido):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener el resumen del partido
    cursor.execute('SELECT COUNT(*) FROM demanda WHERE date = ?', (fecha_partido,))
    count_demanda = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM oferta WHERE date = ?', (fecha_partido,))
    count_oferta = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM oferta WHERE date = ? AND processed = 0', (fecha_partido,))
    entradas_libres_oferta = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM demanda WHERE date = ? AND processed = 0', (fecha_partido,))
    entradas_libres_demanda = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT pedido) FROM demanda WHERE date = ?', (fecha_partido,))
    total_pedidos = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT pedido) FROM demanda WHERE date = ? AND match_names = 1', (fecha_partido,))
    total_pedidos_completados = cursor.fetchone()[0]
    
    cursor.execute('SELECT DISTINCT pedido FROM demanda WHERE date = ? AND match_names = 1', (fecha_partido,))
    pedidos_completados = cursor.fetchall()
    
    cursor.execute('SELECT DISTINCT pedido FROM demanda WHERE date = ? AND match_names = 0', (fecha_partido,))
    pedidos_no_completados = cursor.fetchall()
    
    cursor.execute('SELECT * FROM oferta WHERE date = ?', (fecha_partido,))
    tabla_oferta = cursor.fetchall()
    
    cursor.execute('SELECT * FROM demanda WHERE date = ?', (fecha_partido,))
    tabla_demanda = cursor.fetchall()
    
    conn.close()
    
    # Generar el PDF
    pdf_path = os.path.join(OUTPUT_PEDIDO_DIR, f"reporte_partido_{fecha_partido}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 50, f"Reporte del Partido - {fecha_partido}")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 100, f"Total Demanda: {count_demanda}")
    c.drawString(50, height - 120, f"Total Oferta: {count_oferta}")
    c.drawString(50, height - 140, f"Entradas Libres Oferta: {entradas_libres_oferta}")
    c.drawString(50, height - 160, f"Entradas Libres Demanda: {entradas_libres_demanda}")
    c.drawString(50, height - 180, f"Total Pedidos: {total_pedidos}")
    c.drawString(50, height - 200, f"Total Pedidos Completados: {total_pedidos_completados}")
    
    c.drawString(50, height - 240, "Pedidos Completados:")
    y = height - 260
    col = 0
    for i, pedido in enumerate(pedidos_completados):
        if i % 30 == 0 and i != 0:
            col += 1
            y = height - 260
        c.drawString(70 + col * 150, y, str(pedido[0]))
        y -= 20
    
    c.drawString(50, y - 20, "Pedidos No Completados:")
    y -= 40
    for pedido in pedidos_no_completados:
        c.drawString(70, y, str(pedido[0]))
        y -= 20
    
    c.drawString(50, y - 40, "Tabla Oferta:")
    y -= 60
    for row in tabla_oferta:
        c.drawString(70, y, str(row))
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    
    c.drawString(50, y - 40, "Tabla Demanda:")
    y -= 60
    for row in tabla_demanda:
        c.drawString(70, y, str(row))
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    
    c.save()
    print(f"Reporte generado exitosamente en {pdf_path}")

if __name__ == "__main__":
    fecha_partido = "20250202"  # Reemplaza con la fecha del partido correspondiente
    generar_reporte_partido(fecha_partido)