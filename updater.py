# import pyodbc
# import sqlite3
# def update_db(server,username,password):
#     connectionString = f'DRIVER={"ODBC Driver 17 for SQL Server"};SERVER={server};DATABASE={"Абитуриенты"};UID={username};PWD={password};Trusted_Connection=yes'
#     with pyodbc.connect(connectionString) as conn:
#         SQL_QUERY = """
#             Select distinct А.ID,concat(Имя,' ',Отчество) firstname, Фамилия lastname, E_Mail from Все_Абитуриенты А 
#         join Все_Заявления З on А.ID=З.ID and Год_Набора=year(GetDate()) and ВИ_ДО=1 join Специальности С on З.Код_Специальности=С.Код and Уровень in (1,2) and Иностранец=0;
#             """
#         SQL_QUERY_1="""Select distinct id,concat(test_LN,' ',test_SN) firstname, test_FN lastname, e_mail from test_FIO_ABIT;"""
#         with conn.cursor() as cur:
#             cur.execute(SQL_QUERY)
#             data=cur.fetchall()
            
#     connection=sqlite3.connect("my_db.db")
#     cursor=connection.cursor()
#     for item in data:
#         cursor.execute("select max(id) from users where id_delo not null")
#         id=int(cursor.fetchall()[0][0])+1
#         cursor.execute("select id_delo from users where id_delo not null")
#         users=cursor.fetchall()
#         users=list(map(lambda x: x[0],users))
#         print(id)
#         if item[0] not in users:
#             cursor.execute(f'''
#             update users
#             set id_delo={item[0]}, firstname="{item[1]}",
#             lastname="{item[2]}", email="{item[3]}"
#             where id_delo is Null 
#             and id={id}
#              ''')
#             id+=1
#             connection.commit()
#     connection.close()

import pyodbc
import sqlite3

def update_db(server, username, password):
    # Подключение к SQL Server
    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=Абитуриенты;'
        f'UID={username};PWD={password};Trusted_Connection=yes'
    )
    
    try:
        with pyodbc.connect(connection_string) as conn:
            sql_query = """
                SELECT DISTINCT А.ID, CONCAT(Имя, ' ', Отчество) AS firstname, Фамилия AS lastname, E_Mail
                FROM Все_Абитуриенты А 
                JOIN Все_Заявления З ON А.ID = З.ID AND Год_Набора = YEAR(GETDATE()) AND ВИ_ДО = 1
                JOIN Специальности С ON З.Код_Специальности = С.Код AND Уровень IN (1, 2) AND Иностранец = 0;
            """
            
            with conn.cursor() as cur:
                cur.execute(sql_query)
                data = cur.fetchall()
    except Exception as e:
        print(f"Ошибка при подключении к SQL Server: {e}")
        return

    # Подключение к SQLite и обновление данных
    try:
        connection = sqlite3.connect("my_db.db")
        cursor = connection.cursor()

        for item in data:
            cursor.execute("SELECT MAX(id) FROM users WHERE id_delo IS NOT NULL")
            max_id = cursor.fetchone()[0]
            new_id = max_id + 1 if max_id else 1

            cursor.execute("SELECT id_delo FROM users WHERE id_delo IS NOT NULL")
            existing_users = cursor.fetchall()
            existing_user_ids = [user[0] for user in existing_users]

            if item[0] not in existing_user_ids:
                cursor.execute("""
                    UPDATE users
                    SET id_delo = ?, firstname = ?, lastname = ?, email = ?
                    WHERE id_delo IS NULL AND id = ?
                """, (item[0], item[1], item[2], item[3], new_id))

                connection.commit()

    except Exception as e:
        print(f"Ошибка при обновлении SQLite: {e}")
    finally:
        connection.close()