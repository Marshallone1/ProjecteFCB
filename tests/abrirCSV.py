import csv

def read_csv_file(csv_filepath):
    data = []
    with open(csv_filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)
    return data

if __name__ == "__main__":
    csv_filepath = "C:/Users/Inorbis/ProjecteFCB/data/input/Asignacion/PlantillaBetis.csv"  # Reemplaza con la ruta a tu archivo CSV
    data = read_csv_file(csv_filepath)
    for row in data:
        print(row)
    if data:
        print(f"Claves disponibles: {data[0].keys()}")