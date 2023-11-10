import smtplib
import sqlite3
from email.message import EmailMessage
import working_with_listbox as wwl
def send_email(mail_from,mail_to,password,subject, body):
    mail_to = mail_to if type(mail_to) is list else [mail_to]
    msg = EmailMessage()
    msg['From'] = mail_from
    msg['To'] = ", ".join(mail_to)
    msg['Subject'] = subject
    msg.set_content(body)
    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.login(mail_from,password)
    text = msg.as_string()
    server.sendmail(mail_from, mail_to, text)
    server.quit()
def send_message_to_users(users,mail_from,password):
    connection=sqlite3.connect("my_db.db")
    cursor=connection.cursor()
    for user in users:
        count, lastname, firstname, surname, id_delo=user.split()
        cursor.execute(f"select username, password, email from users where id_delo={id_delo}")
        print(cursor.fetchall())
send_message_to_users(wwl.get_users())
        

