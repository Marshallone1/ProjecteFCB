import re
from transformers import pipeline

# Cargar el pipeline de NER con un modelo público
nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

# Texto de ejemplo
texto = """
Nombre: JIRAN LIM DNI: M175A0564

Nombre: Sangyul Myung DNI: M651Z7506

Nombre: Marcos Llorente DNI: M175A0564
"""

# Realizar la extracción de entidades con el modelo AI
entidades = nlp(texto)

# Regex para identificar patrones de ID (como pasaporte o identificadores nacionales)
id_pattern = r'\b[A-Z]{1,2}\d{5,9}\b|\b\d{5,10}\b'

# Extraer nombres y IDs válidos
valid_names = []
valid_ids = []

# Filtrar nombres válidos y sus IDs
for entidad in entidades:
    if entidad['entity_group'] == 'PER' and len(entidad['word'].split()) >= 2:
        # Buscar el ID más cercano al nombre dentro de un rango de 100 caracteres
        match = re.search(rf'{entidad["word"]}.*?({id_pattern})', texto, re.DOTALL)
        if match:
            valid_names.append(entidad['word'])
            valid_ids.append(match.group(1))
        else:
            # Buscar el ID antes del nombre dentro de un rango de 100 caracteres
            match = re.search(rf'({id_pattern}).*?{entidad["word"]}', texto, re.DOTALL)
            if match:
                valid_names.append(entidad['word'])
                valid_ids.append(match.group(1))

# Emparejar nombres e identificaciones
paired_names_ids = []
for i in range(min(len(valid_names), len(valid_ids))):
    paired_names_ids.append(f"{valid_names[i]} {valid_ids[i]}")

# Mostrar los resultados
print("Nombres e identificaciones extraídos:")
for result in paired_names_ids:
    print(result)