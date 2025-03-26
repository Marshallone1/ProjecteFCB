import os
import sqlite3
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from config import DB_PATH, DATA_DIR, csv_filepath, OUTPUT_PEDIDO_DIR

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
    
    cursor.execute('PRAGMA table_info(oferta)')
    headers_oferta = [info[1] for info in cursor.fetchall()]
    
    cursor.execute('PRAGMA table_info(demanda)')
    headers_demanda = [info[1] for info in cursor.fetchall()]
    
    cursor.execute('SELECT * FROM oferta WHERE date = ?', (fecha_partido,))
    tabla_oferta = cursor.fetchall()
    
    cursor.execute('SELECT * FROM demanda WHERE date = ?', (fecha_partido,))
    tabla_demanda = cursor.fetchall()
   
    #total_pedidos_completados = sum(1 for row in data_with_status[1:] if row[-1] == 'Sí')
    
    # Generar el PDF
    pdf_path = os.path.join(DATA_DIR, f"reporte_partido_{fecha_partido}.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título del reporte
    elements.append(Paragraph(f"Reporte del Partido - {fecha_partido}", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Resumen del partido
    elements.append(Paragraph(f"<b>Total Demanda:</b> <font size=12>{count_demanda}</font>", styles['Normal']))
    elements.append(Paragraph(f"<b>Total Oferta:</b> <font size=12>{count_oferta}</font>", styles['Normal']))
    elements.append(Paragraph(f"<b>Entradas Libres Oferta:</b> <font size=12>{entradas_libres_oferta}</font>", styles['Normal']))
    elements.append(Paragraph(f"<b>Demanda sin entrada:</b> <font size=12>{entradas_libres_demanda}</font>", styles['Normal']))
    elements.append(Paragraph(f"<b>Total Pedidos:</b> <font size=12>{total_pedidos}</font>", styles['Normal']))
    #elements.append(Paragraph(f"<b>Total Pedidos Completados:</b> <font size=12>{total_pedidos_completados}</font>", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Leer y agregar el contenido del archivo CSV en una tabla
    elements.append(Paragraph("Asignación:", styles['Heading2']))
    with open(csv_filepath, newline='', encoding='latin1') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = [row for row in reader]
    
    # Agregar columna adicional para indicar si el pedido está completado
    headers_csv = data[0] + ['Completado']
    data_with_status = [headers_csv]
    
    # Leer los pedidos completados desde OUTPUT_PEDIDO_DIR
    pedidos_completados_set = set()
    for filename in os.listdir(OUTPUT_PEDIDO_DIR):
        if filename.endswith('.pdf'):  # Asumiendo que los pedidos completados están en archivos .pdf
            pedido_id = filename.replace('.pdf', '')
            pedidos_completados_set.add(pedido_id)
    
    for row in data[1:]:
        pedido_id = row[headers_csv.index('PEDIDO')]
        completado = 'Sí' if pedido_id in pedidos_completados_set else 'No'
        data_with_status.append(row + [completado])
    
    table = Table(data_with_status)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 12))
    
    # Aplicar color rojo claro a las filas donde el pedido no está completado
    for i, row in enumerate(data_with_status[1:], start=1):
        if row[-1] == 'No':
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (-1, i), colors.lightcoral),
            ]))
    
    # Tabla Oferta
    elements.append(Paragraph("Tabla Oferta:", styles['Heading2']))
    data = [headers_oferta] + [list(map(str, row)) for row in tabla_oferta]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Aplicar color verde flojo a las filas donde la columna 'processed' es 0
    processed_index = headers_oferta.index('processed')
    for i, row in enumerate(tabla_oferta, start=1):
        if row[processed_index] == 0:
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (-1, i), colors.lightgreen),
            ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    
    # Tabla Demanda
    elements.append(Paragraph("Tabla Demanda:", styles['Heading2']))
    
    # Excluir las columnas 'fecha' y 'id'
    exclude_columns = ['date', 'dni', 'match_names']
    headers_demanda_filtered = [header for header in headers_demanda if header not in exclude_columns]
    data = [headers_demanda_filtered] + [[str(row[headers_demanda.index(header)]) for header in headers_demanda_filtered] for row in tabla_demanda]
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),  # Ajustar el contenido de las celdas
    ]))

    # Aplicar color rojo flojo a las filas donde la columna 'processed' es 0
    processed_index = headers_demanda.index('processed')
    for i, row in enumerate(tabla_demanda, start=1):
        if row[processed_index] == 0:
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (-1, i), colors.lightcoral),
            ]))

    elements.append(table)
    elements.append(Spacer(1, 12))
    
    # Limitar el tamaño de las tablas para que no sobresalgan del tamaño de la página
    if len(data) > 20:
        elements.append(PageBreak())

    doc.build(elements)
    print(f"Reporte generado exitosamente en {pdf_path}")

if __name__ == "__main__":
    fecha_partido = "20250327"  # Reemplaza con la fecha del partido correspondiente
    generar_reporte_partido(fecha_partido)