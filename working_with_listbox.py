# import sqlite3
# import os
# def get_users():
#     if "my_db.db" in os.listdir():
#         connection=sqlite3.connect("my_db.db")
#         cursor=connection.cursor()
#         cursor.execute("select firstname, lastname, number_of_emails_sent, id_delo  from users where id_delo not null")
#         users=cursor.fetchall()
#         users=sorted(users,key=lambda x:(x[2],x[1]))
#         users=list(map(lambda x: str(x[2])+" "+x[1]+" "+x[0]+" "+str(x[3]),users))
#         connection.close()
#         return users
#     else:
#         return []

import sqlite3
import os

def get_users():
    db_path = "my_db.db"
    if os.path.exists(db_path):
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT firstname, lastname, number_of_emails_sent, id_delo 
                FROM users 
                WHERE id_delo IS NOT NULL
            """)
            users = cursor.fetchall()

        # Сортировка пользователей по количеству отправленных писем и фамилии
        users.sort(key=lambda x: (x[2], x[1]))

        # Форматирование списка пользователей
        formatted_users = [f"{user[2]} {user[1]} {user[0]} {user[3]}" for user in users]
        
        return formatted_users
    else:
        return []