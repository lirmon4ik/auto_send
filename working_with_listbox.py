import sqlite3
import os
def get_users():
    if "my_db.db" in os.listdir():
        connection=sqlite3.connect("my_db.db")
        cursor=connection.cursor()
        cursor.execute("select firstname, lastname, number_of_emails_sent, id_delo  from users where id_delo not null")
        users=cursor.fetchall()
        users=sorted(users,key=lambda x:(x[2],x[1]))
        users=list(map(lambda x: str(x[2])+" "+x[1]+" "+x[0]+" "+str(x[3]),users))
        connection.close()
        return users
    else:
        return []
