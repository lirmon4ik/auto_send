import pyodbc
import sqlite3
def update_db(server,database,username,password)
    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connectionString)
    SQL_QUERY = """
        Select distinct А.ID,concat(Имя,' ',Отчество) firstname, Фамилия lastname, E_Mail from Все_Абитуриенты А 
    join Все_Заявления З on А.ID=З.ID and Год_Набора=year(GetDate()) and ВИ_ДО=1 ;
        """
    cur = conn.cursor()
    cur.execute(SQL_QUERY)
    data=cur.fetchall()
    conn.close()
    connection=sqlite3.connect("my_db.db")
    cursor=connection.cursor()
    for item in data:
        cursor.execute("select count(*) from users where id_delo not null")
        id=int(cursor.fetchall()[0][0])+1
        cursor.execute("select id_delo from users where id_delo not null")
        users=cursor.fetchall()
        users=list(map(lambda x: x[0],users))
        if item[0] not in users:
            cursor.execute(f'''
            update users
            set id_delo={item[0]}, firstname="{item[1]}",
            lastname="{item[2]}", email="{item[3]}"
            where id_delo is Null 
            and id={id}
            ''')
            id+=1
            connection.commit()
    connection.close()
