import smtplib
import configparser
from email.message import EmailMessage
def send_email(mail_from,mail_to,subject, body):
    mail_to = mail_to if type(mail_to) is list else [mail_to]
    msg = EmailMessage()
    msg['From'] = mail_from
    msg['To'] = ", ".join(mail_to)
    msg['Subject'] = subject
    msg.set_content(body)
    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.login(mail_from,c['MAIL']['PASSWORD'])
    text = msg.as_string()
    server.sendmail(mail_from, mail_to, text)
    server.quit()
c = configparser.ConfigParser()
c.read('settings.ini')
send_email(c['MAIL']['MAIL_FROM'],c['MAIL']['MAIL_TO'], 'Тестовое сообщение', 'Hello world')
print("Письмо отправлено!")