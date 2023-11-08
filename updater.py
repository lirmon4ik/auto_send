import sqlite3
data=[[123,"Иванов Иван","Иванович","почта@домен"],
[456,"Иванов Иван2","Иванович",""],
[78,"Иванов Иван3","Иванович","почта@домен3"],
[9,"Иванов Иван4","Иванович","почта@домен4"]]
def update_db():
    connection=sqlite3.connect("my_db.db")
    cursor=connection.cursor()
    id=int(cursor.execute("select count(*) from users where id_delo not null").fetchall()[0][0])+1
    for item in data:
        cursor.execute(f'''
        update users
        set id_delo={item[0]}, firstname="{item[1]}",
        lastname="{item[2]}", email="{item[3]}"
        where id_delo is Null 
        and id={id}
        and id_delo not in (select id_delo from users where id_delo is not Null)
        ''')
        connection.commit()
        id+=1
    
    cursor.execute(f'''
    select * from users 
    ''')
    connection.commit()
    for item in cursor.fetchall():
        print(item)
    connection.close()

update_db()

