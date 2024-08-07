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

def add_abit(sender):
    """Функция добавления абитуриента в список."""
    data = dpg.get_value(sender)
    items = dpg.get_item_configuration("lb_2")['items']
    items.append(data)
    dpg.configure_item("lb_2", items=items)
    
    items = dpg.get_item_configuration("lb_1")['items']
    items.remove(data)
    dpg.configure_item("lb_1", items=items)
    dpg.add_text(f"Добавлен абитуриент: {data}", parent="text_parent", color=(0, 255, 0))

def del_abit(sender):
    """Функция удаления абитуриента из списка."""
    data = dpg.get_value(sender)
    items = dpg.get_item_configuration("lb_1")['items']
    items.append(data)
    dpg.configure_item("lb_1", items=items)
    
    items = dpg.get_item_configuration("lb_2")['items']
    items.remove(data)
    dpg.configure_item("lb_2", items=items)
    dpg.add_text(f"Абитуриент удалён: {data}", parent='text_parent', color=(255, 0, 0))

def open_file(sender, app_data):
    """Функция открытия csv файла и занесения данных в БД."""
    try:
        c_db.create_db()
        c_db.read_csv(app_data['file_path_name'])
        dpg.add_text('Данные занесены в БД', parent='text_parent', color=(0, 255, 0))
        dpg.configure_item("open", enabled=False)
    except Exception as e:
        dpg.add_text(f"Ошибка при занесении данных в БД: {e}", parent='text_parent', color=(255, 0, 0))

def send_email():
    """Функция отправки писем абитуриентам."""
    login_email = dpg.get_value("login_email")
    pwd_email = dpg.get_value("pwd_email")
    items = dpg.get_item_configuration("lb_2")['items']
    
    if not (login_email and pwd_email):
        dpg.add_text("Нету данных для входа в почту", parent='text_parent', color=(255, 0, 0))
    else:
        try:
            users = send_message_to_users(items, login_email, pwd_email)
            for user in users:
                if user[1]:
                    dpg.add_text("Письмо отправленно " + user[0], parent='text_parent', color=(0, 255, 0))
                else:
                    dpg.add_text("Письмо не отправленно " + user[0], parent='text_parent', color=(255, 0, 0))
        except Exception as e:
            dpg.add_text(f"Ошибка при отправке писем: {e}", parent='text_parent', color=(255, 0, 0))

def update_DB():
    """Функция обновления данных в БД."""
    if not (dpg.get_value("name") and dpg.get_value("login") and dpg.get_value("pwd")):
        dpg.add_text("Нету данных для соединения к Базе Данных", parent='text_parent', color=(255, 0, 0))
    else:
        try:
            update_db(*dpg.get_values(['name', 'login', 'pwd']))
            dpg.configure_item("lb_1", items=wwl.get_users())
            dpg.add_text("Данные из БД успещно получены", parent='text_parent', color=(0, 255, 0))
        except Exception as e:
            dpg.add_text(f"Ошибка при обновлении БД: {e}", parent='text_parent', color=(255, 0, 0))

def save_settings():
    """Функция сохранения настроек в файл."""
    try:
        settings.set_mssql(*dpg.get_values(['name', 'login', 'pwd']))
        settings.set_mail(dpg.get_value("login_email"), dpg.get_value("pwd_email"))
        dpg.add_text("Настройки успешно сохранены", parent='text_parent', color=(0, 255, 0))
    except Exception as e:
        dpg.add_text(f"Ошибка при сохранении настроек: {e}", parent='text_parent', color=(255, 0, 0))

settings = sett.Settings()  # создаём объект настроек

dpg.create_context()  # создаём контекст

def load_fonts():
    """Загрузка шрифтов для интерфейса."""
    with dpg.font_registry():
        with dpg.font("NotoMono-Regular.ttf", 14, default_font=True) as font1:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    return font1

width = GetSystemMetrics(0)  # получаем ширину экрана
height = GetSystemMetrics(1)  # получаем высоту экрана

def setup_viewport():
    """Настройка и создание окна приложения."""
    dpg.create_viewport(
        title='Custom Title',  # заголовок окна
        width=int(width / 2),
        height=int(height / 2),
        min_width=int(width / 2.5),
        min_height=int(height / 2),
        x_pos=int(width / 2 - width / 5),
        y_pos=int(height / 2 - height / 3.5),
        max_width=int(width / 2.5),
        max_height=int(height / 2)
    )

def create_menu():
    """Создание меню в окне приложения."""
    with dpg.viewport_menu_bar():
        with dpg.menu(label="Settings"):
            with dpg.menu(label="Подключение к БД"):
                dpg.add_input_text(label="Имя Сервера", tag="name", default_value=settings.get_mssql()[0] if settings.is_exist else "")
                dpg.add_input_text(label="Имя пользователя", tag="login", default_value=settings.get_mssql()[1] if settings.is_exist else "")
                dpg.add_input_text(label="Пароль", tag="pwd", password=True, hint="<password>", default_value=settings.get_mssql()[2] if settings.is_exist else "")

def create_main_window():
    """Создание главного окна приложения."""
    with dpg.window(tag="start_window"):
        with dpg.group(horizontal=True):
            lb_1 = dpg.add_listbox(
                items=wwl.get_users(),
                tag='lb_1',
                callback=add_abit,
                width=205,
                pos=[535, 22],
                num_items=18
            )
            lb_2 = dpg.add_listbox(
                items=[],
                tag='lb_2',
                callback=del_abit,
                width=205,
                pos=[320, 22],
                num_items=18
            )
        with dpg.file_dialog(directory_selector=False, show=False, tag="file_dialog_id", width=700, height=400, callback=open_file):
            dpg.add_file_extension(".csv")
        with dpg.child_window(width=310, pos=[8, 22], height=334):
            pass
        with dpg.child_window(width=310, pos=[8, 358], autosize_y=True, tag="text_parent"):
            pass
        with dpg.child_window(width=420, pos=[320, 358], autosize_y=True):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=198, pos=[8, 8], autosize_y=True):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label='Открыть файл', width=94, height=50, tag='open', pos=[1, 4], callback=lambda: dpg.show_item("file_dialog_id"), enabled=not os.path.isfile(os.getcwd() + '\\' + 'my_db.db'))
                        if os.path.isfile(os.getcwd() + '\\' + 'my_db.db'):
                            dpg.add_text('БД уже создана', parent='text_parent', color=(0, 255, 0))
                        else:
                            dpg.add_text('БД не найдена, ... Выберите файл (.*csv)', parent='text_parent', color=(255, 0, 0))
                        dpg.add_button(label='Обновить', tag='update', width=94, height=50, callback=lambda: threading.Thread(target=update_DB).start())
                        dpg.add_button(label='Отправить', tag="send_email", pos=[0, 61], width=95, height=50, callback=lambda: threading.Thread(target=send_email).start())
                        dpg.add_button(label='Сохранить \nнастройки', tag="sett_save", width=95, height=50, callback=save_settings)
                with dpg.child_window(width=198, autosize_y=True):
                    with dpg.group():
                        dpg.add_input_text(label="Логин", tag="login_email", width=128, default_value=settings.get_mail()[0] if settings.is_exist else "")
                        dpg.add_input_text(label="Пароль", tag="pwd_email", password=True, hint="<password>", default_value=settings.get_mail()[1] if settings.is_exist else "")

def main():
    """Основная функция для запуска приложения."""
    font1 = load_fonts()
    dpg.bind_font(font1)
    dpg.create_context()
    setup_viewport()
    create_menu()
    create_main_window()
    
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("start_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()
