import sqlite3
def update_db():
    connection=sqlite3.connect("my_db.db")
    cursor=connection.cursor()
    cursor.execute("select count(*) from users where id_delo not null")
    id=int(cursor.fetchall()[0][0])+1
    cursor.execute("select id_delo from users where id_delo not null")
    users=cursor.fetchall()
    users=list(map(lambda x: x[0],users))
    for item in data:
        print(item[0],users)
        if item[0] not in users:
            print(True)
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

