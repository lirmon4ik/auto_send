# -*- coding: utf-8 -*-

from dearpygui.dearpygui import (get_item_configuration, configure_item, add_text, get_value, get_values, create_context,
                                 font_registry, font, add_font_range_hint, create_viewport, mvFontRangeHint_Cyrillic, 
                                 viewport_menu_bar,menu,add_input_text,window,group,add_listbox,file_dialog,
                                 add_file_extension,child_window,add_button,bind_font,setup_dearpygui,show_viewport,
                                 set_primary_window,start_dearpygui,destroy_context,show_item)
from win32api import GetSystemMetrics
import creator_db as c_db
from os.path import isfile
from os import getcwd
import working_with_listbox as wwl
from updater import update_db
from sender_message import send_message_to_users
import save_settings as sett
from threading import Thread


def add_abit(sender, data):  # функция добавления абитуриента в список
    items = get_item_configuration("lb_2")['items']
    items.append(data)
    configure_item("lb_2", items=items)

    items = get_item_configuration("lb_1")['items']
    items.remove(data)
    configure_item("lb_1", items=items)
    add_text(f"Добавлен абитуриент: {data} ",
             parent="text_parent", color=(0, 255, 0))


def del_abit(sender, data):  # функция удаления абитуриента из списка
    items = get_item_configuration("lb_1")['items']
    items.append(data)
    configure_item("lb_1", items=items)

    items = get_item_configuration("lb_2")['items']
    items.remove(data)
    configure_item("lb_2", items=items)
    add_text(f"Абитуриент удалён: {data} ",
             parent='text_parent', color=(255, 0, 0))


def open_file(sender,app_data,user_data):  # функция открытия csv файла
    print(app_data['selections'][app_data['file_name']])
    c_db.create_db()
    c_db.read_csv(app_data['selections'][app_data['file_name']])
    add_text('Данные занесены в БД',
             parent='text_parent', color=(0, 255, 0))
    configure_item("open", enabled=False)


def send_email():  # функция отправки писем в почту
    login_email = get_value("login_email")
    pwd_email = get_value("pwd_email")
    items = get_item_configuration("lb_2")['items']

    if not (login_email and pwd_email):
        add_text("Нету данных для входа в почту",
                 parent='text_parent', color=(255, 0, 0))
    else:
        users = send_message_to_users(items, login_email, pwd_email)
        for user in users:
            if user[1]:
                add_text("Письмо отправленно " +
                         user[0], parent='text_parent', color=(0, 255, 0))
            else:
                add_text("Письмо не отправленно " +
                         user[0], parent='text_parent', color=(255, 0, 0))


def update_DB():  # функция обновления данных в БД
    if not (get_value("name") and get_value("login") and get_value("pwd")):
        add_text("Нету данных для соединения к Базе Данных",
                 parent='text_parent', color=(255, 0, 0))
    else:
        update_db(*get_values(['name', 'login', 'pwd']))
        configure_item("lb_1", items=wwl.get_users())
        add_text("Данные из БД успешно получены",
                 parent='text_parent', color=(0, 255, 0))


def save_settings():  # функция сохранения настроек в файл
    settings.set_mssql(*get_values(['name', 'login', 'pwd']))
    settings.set_mail(get_value("login_email"), get_value("pwd_email"))


settings = sett.Settings()  # создаём объект настроек

create_context()  # создаём контекст

with font_registry():  # загружаем шрифты
    with font("NotoMono-Regular.ttf", 14, default_font=True) as font1:
        add_font_range_hint(mvFontRangeHint_Cyrillic)

width = GetSystemMetrics(0)  # получаем ширину системы
height = GetSystemMetrics(1)  # получаем высоту системы


create_viewport(title='Custom Title',  # заголовок окна
                width=int(width/2),
                height=int(height/2),
                min_width=int(width/2.5),
                min_height=int(height/2),
                x_pos=int(width/2-width/5),
                y_pos=int(height/2-height/3.5),
                max_width=int(width/2.5),
                max_height=int(height/2)
                )

with viewport_menu_bar():  # создаём меню
    with menu(label="Settings"):  # создаём меню настроек
        with menu(label="Подключение к БД"):
            add_input_text(label="Имя Сервера", tag="name", default_value=settings.get_mssql()[
                               0] if settings.is_exist else "")  # поле ввода имени сервера
            add_input_text(label="Имя пользователя", tag="login", default_value=settings.get_mssql()[
                               1] if settings.is_exist else "")  # поле ввода имени пользователя
            add_input_text(label="Пароль", tag="pwd",
                               password=True, hint="<password>", default_value=settings.get_mssql()[2] if settings.is_exist else "")  # поле ввода пароля


with window(tag="start_window"):  # создаём окно

    with group(horizontal=True):  # создаём группу
        add_listbox(items=wwl.get_users(),  # создаём основной список абитуриентов
                        tag='lb_1',
                        callback=add_abit,
                        width=205,
                        pos=[535, 22],
                        num_items=18
                        )
        add_listbox(items=[],  # создаём второстепенный список абитуриентов
                        tag='lb_2',
                        callback=del_abit,
                        width=205,
                        pos=[320, 22],
                        num_items=18
                        )

    # создаём окно для выбора файла
    with file_dialog(directory_selector=False, show=False, tag="file_dialog_id", width=700, height=400, callback=open_file):
        add_file_extension(".csv")

    # создаём окно для вывода данных о абитуриентах
    with child_window(width=310, pos=[8, 22], height=334):
        pass

    # создаём окно для логирования абитуриентов
    with child_window(width=310, pos=[8, 358], autosize_y=True, tag="text_parent"):
        pass

    # создаём дочернее окно
    with child_window(width=420, pos=[320, 358], autosize_y=True):
        with group(horizontal=True):  # создаём группу
            # создаём дочернее окно
            with child_window(width=198, pos=[8, 8], autosize_y=True):
                # создаём группу с горизонтальной группировкой
                with group(horizontal=True):
                    add_button(label='Открыть файл', width=94, height=50, tag='open', pos=[1, 4], callback=lambda: show_item(
                        "file_dialog_id"), enabled=not isfile(getcwd()+'\\'+'my_db.db'))  # создаём кнопку для открытия файла
                    # проверяем, есть ли база данных
                    if isfile(getcwd()+'\\'+'my_db.db'):
                        add_text('БД уже создана',
                                     parent='text_parent', color=(0, 255, 0))
                    else:
                        add_text('БД не найдена, ... Выберите файл (.*csv)',
                                     parent='text_parent', color=(255, 0, 0))
                    add_button(label='Обновить', tag='update',
                                   width=94, height=50, callback=lambda: Thread(target=update_DB).start())  # создаём кнопку для обновления данных
                    add_button(label='Отправить',
                                   tag="send_email", pos=[0, 61], width=95, height=50, callback=lambda: Thread(target=send_email).start())  # создаём кнопку для отправки писем
                    add_button(label='Сохранить \nнастройки',
                                   tag="sett_save", width=95, height=50, callback=save_settings)  # создаём кнопку для сохранения настройки
            with child_window(width=198, autosize_y=True):  # создаём дочернее окно
                with group():  # создаём группу
                    add_input_text(
                        label="Логин", tag="login_email", width=128, default_value=settings.get_mail()[0] if settings.is_exist else "")  # поле ввода логина пользователя
                    add_input_text(
                        label="Пароль", tag="pwd_email", password=True, hint="<password>", default_value=settings.get_mail()[1] if settings.is_exist else "")  # поле ввода пароля

    bind_font(font1)  # запускаем функцию для загрузки шрифта

if __name__ == '__main__':  # точка входа в программу
    setup_dearpygui()  # задаём настройки окна
    show_viewport()  # отображаем окно
    # делаем окно в основном окне главным
    set_primary_window("start_window", True)
    start_dearpygui()  # запускаем программу
    destroy_context()  # останавливаем контекст
