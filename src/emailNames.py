import imaplib
import email
from email.header import decode_header
import re
from unidecode import unidecode

def extract_names_from_body(body):
    # Buscar patrones específicos en el cuerpo del mensaje
    pattern = re.compile(r'Nombre Completo:\s*\*([^\*]+)\*')
    names = pattern.findall(body)
    # Convertir a mayúsculas y eliminar tildes
    names = [unidecode(name).upper() for name in names]
    return names

def get_names_from_email(imap_server, email_user, email_pass, subject_id):
    try:
        # Conectarse al servidor IMAP
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)

        mail.select("inbox")

        # Buscar el correo electrónico por Asunto
        status, messages = mail.search(None, f'(SUBJECT "{subject_id}")')
        if status != "OK":
            return []

        # Obtener el correo electrónico
        email_ids = messages[0].split()
        names = []
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        names.extend(extract_names_from_body(body))
            else:
                body = msg.get_payload(decode=True).decode()
                names.extend(extract_names_from_body(body))

        return names
    except Exception as e:
        print(f"Error al obtener nombres del correo: {e}")
        return []