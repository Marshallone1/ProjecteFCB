import csv
import sqlite3
from src.emailNames import get_names_from_email
from src.config import imap_server, email_user, email_pass, csv_filepath

# Función para leer datos reales desde un archivo CSV
def read_real_data_from_csv(csv_filepath):
    real_data = []
    with open(csv_filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            real_data.append(row)
    return real_data

# Función para generar datos de demanda reales
def generate_real_demand(csv_filepath, imap_server, email_user, email_pass):
    # Conectar a la base de datos
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    # Leer datos desde el archivo CSV
    data = read_real_data_from_csv(csv_filepath)

    for row in data:
        print(f"Procesando pedido: {row['PEDIDO']}")
        grupos = int(row['GRUPOS'])
        categoria = row['Categoría (Libre)']
        asientos = row['ASIENTOS'].split('+')
        pedido_id = row['PEDIDO']
        fecha_id = row['FECHAID']

        # Obtener nombres de los correos electrónicos
        names = get_names_from_email(imap_server, email_user, email_pass, pedido_id)
        print(f"Nombres obtenidos: {names}")
        name_index = 0

        # Asignar nombres y DNIs a las entradas
        for asiento_group in asientos:
            asiento_list = asiento_group.split('-')
            for asiento in asiento_list:
                parts = asiento.split('.')
                if len(parts) == 3:
                    boca, fila, asiento_num = parts
                elif len(parts) == 1:
                    asiento_num = parts[0]
                else:
                    cursor.execute('''
                        INSERT INTO demanda (date, boca, fila, asiento, name, dni, pedido, processed, match_names)
                        VALUES (?, NULL, NULL, NULL, NULL, NULL, ?, 0, 0)
                    ''', (fecha_id, pedido_id))
                    continue

                name = names[name_index] if name_index < len(names) else None
                dni = ""  # Dejar el campo dni en blanco
                match_names = 1 if name else 0
                print(f"Insertando en la base de datos: fecha_id={fecha_id}, boca={boca}, fila={fila}, asiento={asiento_num}, name={name}, pedido_id={pedido_id}, match_names={match_names}")
                cursor.execute('''
                    INSERT INTO demanda (date, boca, fila, asiento, name, dni, pedido, processed, match_names)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
                ''', (fecha_id, boca, fila, asiento_num, name, dni, pedido_id, match_names))
                name_index += 1

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == "__main__":

    # Generar demanda real
    generate_real_demand(csv_filepath, imap_server, email_user, email_pass)
    print("Datos de demanda reales generados exitosamente.")