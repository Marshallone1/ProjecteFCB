import imaplib
import email
from email.header import decode_header
import re
from unidecode import unidecode

def extract_names_from_body(body):
    # Buscar patrones específicos en el cuerpo del mensaje
    pattern = re.compile(r'Nombre Completo:\s*(.*?)\s*Fecha de Nacimiento:')    
    names = pattern.findall(body)
    # Convertir a mayúsculas y eliminar tildes y asteriscos
    names = [unidecode(name).upper().replace('*', '') for name in names]
    return names

def test_email_connection(imap_server, email_user, email_pass, subject_id):
    try:
        # Conectarse al servidor IMAP
        print("Conectando al servidor IMAP...")
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        print("Conexión exitosa.")

        mail.select("inbox")

        # Buscar el correo electrónico por Asunto
        print(f"Buscando el correo electrónico con Asunto que contiene: {subject_id}")
        status, messages = mail.search(None, f'(SUBJECT "{subject_id}")')
        if status != "OK":
            print("No se encontró el correo electrónico.")
            return

        # Obtener el correo electrónico
        email_ids = messages[0].split()
        if not email_ids:
            print("No se encontró el correo electrónico.")
            return

        print(f"Correo electrónico encontrado, ID: {email_ids[0]}")
        status, msg_data = mail.fetch(email_ids[0], "(RFC822)")
        if status != "OK":
            print("Error al obtener el correo electrónico.")
            return

        msg = email.message_from_bytes(msg_data[0][1])
        mail.logout()

        # Extraer el contenido del correo electrónico
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print("Contenido del correo electrónico:")
                    print(body)  # Imprimir todo el contenido del cuerpo del mensaje
                    names = extract_names_from_body(body)
                    print("Nombres extraídos:")
                    print(names)
                    break
        else:
            body = msg.get_payload(decode=True).decode()
            print("Contenido del correo electrónico:")
            print(body)  # Imprimir todo el contenido del cuerpo del mensaje
            names = extract_names_from_body(body)
            print("Nombres extraídos:")
            print(names)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Configuración del servidor de correo
    imap_server = "imap.gmail.com"
    email_user = "registros.ventas.completadas@gmail.com"
    email_pass = "lghe mzod iqed yfzw"  # Asegúrate de usar una contraseña de aplicación si usas Gmail
    subject_id = "554218689"  # Reemplaza con el identificador en el asunto del correo electrónico que deseas probar

    # Probar la conexión y extracción del correo electrónico
    test_email_connection(imap_server, email_user, email_pass, subject_id)