import smtplib
import sqlite3
from email.message import EmailMessage
def send_email(mail_from,mail_to,password,subject, body):
    mail_to = mail_to if type(mail_to) is list else [mail_to]
    msg = EmailMessage()
    msg['From'] = mail_from
    msg['To'] = ", ".join(mail_to)
    msg['Subject'] = subject
    msg.set_content(body,subtype='html')
    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.login(mail_from,password)
    server.send_message(msg)
    server.quit()
def send_message_to_users(users,mail_from,password):
    connection=sqlite3.connect("my_db.db")
    cursor=connection.cursor()
    users_to_send=list()
    users_to_send_complete=list()
    for user in users:
        lastname, firstname, surname, id_delo=user.split()[1:]
        cursor.execute(f"select username, password, email from users where id_delo={id_delo}")
        users_to_send.append((cursor.fetchall()[0],lastname,firstname))
    subject="Логин и пароль для дистанционной сдачи ВИ"
    with open("message.html", encoding="utf-8") as f: 
        message=f.read().strip()
    for user in users_to_send:
        if user[0][2]=="None":
            users_to_send_complete.append((f"{lastname} {firstname}",False))
            continue
        message_copy=message
        message_copy=message_copy.replace("login",user[0][0])
        message_copy=message_copy.replace("password",user[0][1])
        send_email(mail_from,user[0][2],password,subject,message_copy)
        users_to_send_complete.append((f"{user[1]} {user[2]}",True))
    return users_to_send_complete
