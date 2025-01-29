import csv
from src.emailNames import get_names_from_email

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
    # Leer datos desde el archivo CSV
    data = read_real_data_from_csv(csv_filepath)

    for row in data:
        print(row)  # Agregar esta línea para depuración
        grupos = int(row['GRUPOS'])
        categoria = row['Categoría (Libre)']
        asientos = row['ASIENTOS'].split('+')
        pedido_id = row['PEDIDO']
        fecha_id = row['FECHAID']

        # Verificar que la fecha no esté vacía
        if not fecha_id:
            print(f"Error: Fecha vacía para el pedido {pedido_id}")
            print(f"INSERT INTO demanda (date, boca, fila, asiento, name, dni, processed, match_names) VALUES ({fecha_id}, NULL, NULL, NULL, NULL, NULL, 0, 0)")
            continue

        # Obtener nombres desde el correo electrónico
        names = get_names_from_email(imap_server, email_user, email_pass, pedido_id)
        if len(names) < grupos:
            print(f"Error: No hay suficientes nombres para el pedido {pedido_id}. Marcado como no procesado.")
            for asiento_group in asientos:
                asiento_list = asiento_group.split('-')
                for asiento in asiento_list:
                    parts = asiento.split('.')
                    if len(parts) == 3:
                        boca, fila, asiento_num = parts
                        print(f"INSERT INTO demanda (date, boca, fila, asiento, name, dni, processed, match_names) VALUES ({fecha_id}, {boca}, {fila}, {asiento_num}, NULL, NULL, 0, 0)")
                    else:
                        print(f"Error: Formato de asiento incorrecto para el pedido {pedido_id}, asiento: {asiento}")
                        print(f"INSERT INTO demanda (date, boca, fila, asiento, name, dni, processed, match_names) VALUES ({fecha_id}, NULL, NULL, NULL, NULL, NULL, 0, 0)")
            continue

        # Asignar nombres y DNIs a las entradas
        name_index = 0
        for asiento_group in asientos:
            asiento_list = asiento_group.split('-')
            for asiento in asiento_list:
                parts = asiento.split('.')
                if len(parts) == 3:
                    boca, fila, asiento_num = parts
                elif len(parts) == 1:
                    asiento_num = parts[0]
                    boca, fila = None, None
                else:
                    print(f"Error: Formato de asiento incorrecto para el pedido {pedido_id}, asiento: {asiento}")
                    print(f"INSERT INTO demanda (date, boca, fila, asiento, name, dni, processed, match_names) VALUES ({fecha_id}, NULL, NULL, NULL, NULL, NULL, 0, 0)")
                    continue

                name = names[name_index] if name_index < len(names) else None
                dni = f"DNI{pedido_id}{name_index+1}" if name else None
                print(f"INSERT INTO demanda (date, boca, fila, asiento, name, dni, processed, match_names) VALUES ({fecha_id}, {boca}, {fila}, {asiento_num}, {name}, {dni}, 0, 1)")
                name_index += 1

if __name__ == "__main__":
    # Configuración del servidor de correo
    imap_server = "imap.gmail.com"
    email_user = "registros.ventas.completadas@gmail.com"
    email_pass = "lghe mzod iqed yfzw"  # Asegúrate de usar una contraseña de aplicación si usas Gmail

    # Ruta al archivo CSV
    csv_filepath = "C:/Users/Inorbis/ProjecteFCB/data/input/Asignacion/PlantillaBetis.csv"

    # Generar demanda real
    generate_real_demand(csv_filepath, imap_server, email_user, email_pass)
    print("Datos de demanda reales generados exitosamente.")