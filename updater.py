from pyodbc import connect as mssql
from sqlite3 import connect as sq3
def update_db(server,username,password):
    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};UID={username};PWD={password}'
    conn = mssql(connectionString)
    SQL_QUERY = """
        Select distinct А.ID,concat(Имя,' ',Отчество) firstname, Фамилия lastname, E_Mail from Все_Абитуриенты А 
    join Все_Заявления З on А.ID=З.ID and Год_Набора=year(GetDate()) and ВИ_ДО=1 join Специальности С on З.Код_Специальности=С.Код and Уровень in (1,2) ;
        """
    SQL_QUERY_1="""Select distinct id,concat(test_LN,' ',test_SN) firstname, test_FN lastname, e_mail from test_FIO_ABIT;"""
    cur = conn.cursor()
    cur.execute(SQL_QUERY_1)
    data=cur.fetchall()
    conn.close()
    connection=sq3("my_db.db")
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
