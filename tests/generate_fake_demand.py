import sqlite3
from src.databaseSetup import setup_database

# Asegurarse de que la base de datos esté configurada
setup_database()

# Nombres y DNIs falsos
fake_names_dnis = [
    ("John Doe", "12345678A"),
    ("Jane Smith", "23456789B"),
    ("Alice Johnson", "34567890C"),
    ("Bob Brown", "45678901D"),
    ("Charlie Davis", "56789012E")
]

# Función para generar datos de demanda falsos
def generate_fake_demand():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    # Obtener todas las entradas de la tabla oferta
    cursor.execute('SELECT id, date, boca, fila, asiento FROM oferta WHERE processed = 0')
    oferta_entries = cursor.fetchall()

    # Asignar nombres y DNIs a las entradas
    for i, entry in enumerate(oferta_entries):
        id, date, boca, fila, asiento = entry
        name, dni = fake_names_dnis[i % len(fake_names_dnis)]
        # Verificar si la entrada ya existe en la tabla demanda
        cursor.execute('''
            SELECT COUNT(*) FROM demanda WHERE date = ? AND boca = ? AND fila = ? AND asiento = ?
        ''', (date, boca, fila, asiento))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO demanda (date, boca, fila, asiento, name, dni, processed)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            ''', (date, boca, fila, asiento, name, dni))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    generate_fake_demand()
    print("Datos de demanda falsos generados y guardados en la base de datos.")