# -*- coding: utf-8 -*-

import dearpygui.dearpygui as dpg
from win32api import GetSystemMetrics
import creator_db as c_db
import os
import working_with_listbox as wwl
from updater import update_db
from sender_message import send_message_to_users
import save_settings as sett
import threading


def add_abit(sender):  # функция добавления абитуриента в список
    data=dpg.get_value(sender)
    items = dpg.get_item_configuration("lb_2")['items']
    items.append(data)
    print(data)
    dpg.configure_item("lb_2", items=items)

    items=dpg.get_item_configuration("lb_1")['items']
    items.remove(data)
    dpg.configure_item("lb_1", items=items)
    dpg.add_text(f"Добавлен абитуриент: {data} ",
                 parent="text_parent", color=(0, 255, 0))



def del_abit(sender):  # функция удаления абитуриента из списка
    data=dpg.get_value(sender)
    items = dpg.get_item_configuration("lb_1")['items']
    items.append(data)
    dpg.configure_item("lb_1", items=items)

    items = dpg.get_item_configuration("lb_2")['items']
    items.remove(data)
    dpg.configure_item("lb_2", items=items)
    dpg.add_text(f"Абитуриент удалён: {data} ",
                 parent='text_parent', color=(255, 0, 0))


def open_file(sender,app_data):  # функция открытия csv файла

    c_db.create_db()
    c_db.read_csv(app_data['file_path_name'])
    dpg.add_text('Данные занесены в БД',
                 parent='text_parent', color=(0, 255, 0))
    dpg.configure_item("open", enabled=False)


def send_email():  # функция отправки писем в почту
    login_email = dpg.get_value("login_email")
    pwd_email = dpg.get_value("pwd_email")
    items = dpg.get_item_configuration("lb_2")['items']

    if not (login_email and pwd_email):
        dpg.add_text("Нету данных для входа в почту",
                     parent='text_parent', color=(255, 0, 0))
    else:
        users = send_message_to_users(items, login_email, pwd_email)
        for user in users:
            if user[1]:
                dpg.add_text("Письмо отправленно " +
                             user[0], parent='text_parent', color=(0, 255, 0))
            else:
                dpg.add_text("Письмо не отправленно " +
                             user[0], parent='text_parent', color=(255, 0, 0))


def update_DB():  # функция обновления данных в БД
    if not (dpg.get_value("name") and dpg.get_value("login") and dpg.get_value("pwd")):
        dpg.add_text("Нету данных для соединения к Базе Данных",
                     parent='text_parent', color=(255, 0, 0))
    else:
        update_db(*dpg.get_values(['name', 'login', 'pwd']))
        dpg.configure_item("lb_1", items=wwl.get_users())
        dpg.add_text("Данные из БД успещно получены",
                     parent='text_parent', color=(0, 255, 0))


def save_settings():  # функция сохранения настроек в файл
    settings.set_mssql(*dpg.get_values(['name', 'login', 'pwd']))
    settings.set_mail(dpg.get_value("login_email"), dpg.get_value("pwd_email"))


settings = sett.Settings()  # создаём объект настроек

dpg.create_context()  # создаём контекст

with dpg.font_registry():  # загружаем шрифты
    with dpg.font("NotoMono-Regular.ttf", 14, default_font=True) as font1:

        # add the default font range
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        # helper to add range of characters
        #    Options:
        #        mvFontRangeHint_Japanese
        #        mvFontRangeHint_Korean
        #        mvFontRangeHint_Chinese_Full
        #        mvFontRangeHint_Chinese_Simplified_Common
        #        mvFontRangeHint_Cyrillic
        #        mvFontRangeHint_Thai
        #        mvFontRangeHint_Vietnamese
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

width = GetSystemMetrics(0)  # получаем ширину системы
height = GetSystemMetrics(1)  # получаем высоту системы


dpg.create_viewport(title='Custom Title',  # заголовок окна
                    width=int(width/2),
                    height=int(height/2),
                    min_width=int(width/2.5),
                    min_height=int(height/2),
                    x_pos=int(width/2-width/5),
                    y_pos=int(height/2-height/3.5),
                    max_width=int(width/2.5),
                    max_height=int(height/2)
                    )

with dpg.viewport_menu_bar():  # создаём меню
    with dpg.menu(label="Settings"):  # создаём меню настроек
        with dpg.menu(label="Подключение к БД"):
            dpg.add_input_text(label="Имя Сервера", tag="name", default_value=settings.get_mssql()[
                               0] if settings.is_exist else "")  # поле ввода имени сервера
            dpg.add_input_text(label="Имя пользователя", tag="login", default_value=settings.get_mssql()[
                               1] if settings.is_exist else "")  # поле ввода имени пользователя
            dpg.add_input_text(label="Пароль", tag="pwd",
                               password=True, hint="<password>", default_value=settings.get_mssql()[2] if settings.is_exist else "")  # поле ввода пароля


with dpg.window(tag="start_window"):  # создаём окно

    with dpg.group(horizontal=True):  # создаём группу
        lb_1=dpg.add_listbox(items=wwl.get_users(),  # создаём основной список абитуриентов
                        tag='lb_1',
                        callback=add_abit,
                        width=205,
                        pos=[535, 22],
                        num_items=18
                        )
        lb_2=dpg.add_listbox(items=[],  # создаём второстепенный список абитуриентов
                        tag='lb_2',
                        callback=del_abit,
                        width=205,
                        pos=[320, 22],
                        num_items=18
                        )

    # создаём окно для выбора файла
    with dpg.file_dialog(directory_selector=False, show=False, tag="file_dialog_id", width=700, height=400, callback=open_file):
        dpg.add_file_extension(".csv")

    # создаём окно для вывода данных о абитуриентах
    with dpg.child_window(width=310, pos=[8, 22], height=334):
        pass

    # создаём окно для логирования абитуриентов
    with dpg.child_window(width=310, pos=[8, 358], autosize_y=True, tag="text_parent"):
        pass

    # создаём дочернее окно
    with dpg.child_window(width=420, pos=[320, 358], autosize_y=True):
        with dpg.group(horizontal=True):  # создаём группу
            # создаём дочернее окно
            with dpg.child_window(width=198, pos=[8, 8], autosize_y=True):
                # создаём группу с горизонтальной группировкой
                with dpg.group(horizontal=True):
                    dpg.add_button(label='Открыть файл', width=94, height=50, tag='open', pos=[1, 4], callback=lambda: dpg.show_item(
                        "file_dialog_id"), enabled=not os.path.isfile(os.getcwd()+'\\'+'my_db.db'))  # создаём кнопку для открытия файла
                    # проверяем, есть ли база данных
                    if os.path.isfile(os.getcwd()+'\\'+'my_db.db'):
                        dpg.add_text('БД уже создана',
                                     parent='text_parent', color=(0, 255, 0))
                    else:
                        dpg.add_text('БД не найдена, ... Выберите файл (.*csv)',
                                     parent='text_parent', color=(255, 0, 0))
                    dpg.add_button(label='Обновить', tag='update',
                                   width=94, height=50, callback=lambda: threading.Thread(target=update_DB).start())  # создаём кнопку для обновления данных
                    dpg.add_button(label='Отправить',
                                   tag="send_email", pos=[0, 61], width=95, height=50, callback=lambda: threading.Thread(target=send_email).start())  # создаём кнопку для отправки писем
                    dpg.add_button(label='Сохранить \nнастройки',
                                   tag="sett_save", width=95, height=50, callback=save_settings)  # создаём кнопку для сохранения настройки
            with dpg.child_window(width=198, autosize_y=True):  # создаём дочернее окно
                with dpg.group():  # создаём группу
                    dpg.add_input_text(
                        label="Логин", tag="login_email", width=128, default_value=settings.get_mail()[0] if settings.is_exist else "")  # поле ввода логина пользователя
                    dpg.add_input_text(
                        label="Пароль", tag="pwd_email", password=True, hint="<password>", default_value=settings.get_mail()[1] if settings.is_exist else "")  # поле ввода пароля

    dpg.bind_font(font1)  # запускаем функцию для загрузки шрифта

if __name__ == '__main__':  # точка входа в программу
    dpg.setup_dearpygui()  # задаём настройки окна
    dpg.show_viewport()  # отображаем окно
    # делаем окно в основном окне главным
    dpg.set_primary_window("start_window", True)
    dpg.start_dearpygui()  # запускаем программу
    dpg.destroy_context()  # останавливаем контекст
