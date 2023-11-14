import sqlite3 
import csv
# Сперва вызываем функцию create_db для создания бд
# Затем вызываем функцию read_csv для заполнения бд
def create_db():
    connection=sqlite3.connect("my_db.db")
    cursor=connection.cursor()
    cursor.execute('drop table if exists users')
    connection.commit()
    cursor.execute('''
    create table if not exists users(
    id integer primary key autoincrement,
    id_delo integer default null unique,
    username text not null,
    password text not null,
    firstname text default null,
    lastname text default null,
    email text default null,
    cohort1 text,
    department text,
    number_of_emails_sent int default 0)
    ''')
    connection.commit()
    connection.close()
def update_db(reader):
    connection=sqlite3.connect("my_db.db")
    cursor=connection.cursor()
    for row in reader:
        cursor.execute(f'''
        insert into users(username, password,firstname,lastname,email,cohort1,department)
        values ('{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}')
        ''')
        connection.commit()
    connection.close()
def read_csv(file):
    with open(file,encoding='utf-8') as f:
        reader=csv.reader(f,delimiter=';',quotechar='"') 
        headers=next(reader)
        update_db(reader)
        #print("Данные занесены в бд")
