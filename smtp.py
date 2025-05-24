import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

config = {}
with open('config.txt', encoding='utf-8') as f:
    for line in f:
        if ':' in line:
            key, value = line.strip().split(':', 1)
            config[key.strip().lower()] = value.strip()

from_addr = config['from']
password = config['password']
to_addrs = [email.strip() for email in config['to'].split(',')]
subject = config['subject']
attachments = [f.strip() for f in config.get('attachments', '').split(',') if f.strip()]

with open('msg.txt', encoding='utf-8') as f:
    message_body = f.read()

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = ', '.join(to_addrs)
msg['Subject'] = subject
msg.attach(MIMEText(message_body, 'plain', 'utf-8'))

for filename in attachments:
    filepath = os.path.join(filename)
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)
    else:
        print(f"Файл {filename} не найден")

try:
    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addrs, msg.as_string())
        print("Сообщение отправлено")
except Exception as e:
    print("Ошибка:", e)
