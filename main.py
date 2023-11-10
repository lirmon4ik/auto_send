# -*- coding: utf-8 -*-

import dearpygui.dearpygui as dpg
from win32api import GetSystemMetrics
import creator_db as c_db
import os
import working_with_listbox as wwl
from updater import update_db


os.path.isfile(os.getcwd()+'\\'+'my_db.db')

dpg.create_context()
 
with dpg.font_registry():
	with dpg.font("NotoMono-Regular.ttf", 12, default_font=True) as font1:

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
    

width=GetSystemMetrics(0)
height=GetSystemMetrics(1)

print(width, height)



def add_abit(sender, data):
    items = dpg.get_item_configuration("lb_2")['items']
    items.append(data)
    dpg.configure_item("lb_2", items=items)

    
    items = dpg.get_item_configuration("lb_1")['items']
    items.remove(data)
    dpg.configure_item("lb_1", items=items)

    dpg.configure_item("log", color=(0,255,0))
    #dpg.set_value('log', f"Добавлен абитуриент: {data} ")
    dpg.add_text('log',f"Добавлен абитуриент: {data} ")

def del_abit(sender, data):
    items = dpg.get_item_configuration("lb_1")['items']
    items.append(data)
    dpg.configure_item("lb_1", items=items)

    
    items = dpg.get_item_configuration("lb_2")['items']
    items.remove(data)
    dpg.configure_item("lb_2", items=items)

    dpg.configure_item("log", color=(255,0,0))
    dpg.set_value('log', f"Абитуриент удалён: {data} ")


def open_file(sender, app_data, user_data):
    #print("Sender: ", sender)
    c_db.create_db()
    c_db.read_csv(app_data['selections'][app_data['file_name']])
    dpg.configure_item("log", color=(0,255,0))
    dpg.set_value('log', 'Данные занесены в БД')
    
    
    
dpg.create_viewport(title='Custom Title', 
                    width=int(width/2), 
                    height=int(height/2),
                    min_width=int(width/2.5),
                    min_height=int(height/2),
                    x_pos=int(width/4),
                    y_pos=int(height/4),
                    max_width=int(width/2.5),
                    max_height=int(height/2))


with dpg.viewport_menu_bar():
    with dpg.menu(label="Settings"):
        with dpg.menu(label="Подключение к БД"):
            dpg.add_input_text(label="Имя Сервера", tag="name")
            dpg.add_input_text(label="Имя пользователя", tag="login")
            dpg.add_input_text(label="Пароль",tag="pwd", password=True, hint="<password>")
            #dpg.add_input_text(label="База данных",tag="BD")
            
                    
            





with dpg.window(tag="start_window"):
        
        with dpg.group(horizontal=True):
            dpg.add_listbox(items=wwl.get_users(), 
                            tag='lb_1', 
                            callback=add_abit,
                            width=205,
                            pos=[535,23],
                            num_items=20
                            )
            dpg.add_listbox(items=[],
                            tag='lb_2',
                            callback=del_abit,
                            width=205,
                            pos=[320,23],
                            num_items=20
                            )
        with dpg.file_dialog(directory_selector=False, show=False, tag="file_dialog_id", width=700 ,height=400, callback=open_file):
            dpg.add_file_extension(".csv")
            
        with dpg.child_window(width=305, pos=[8,23], height=330):
            dpg.add_text(tag='text_output',wrap=1)
        with dpg.child_window(width=305, pos=[8,360], autosize_y=True):
            dpg.add_text(tag='log',wrap=250,color=(0,0,0))
        with dpg.child_window(width=420, pos=[320,360], autosize_y=True):
            with dpg.child_window(width=198, pos=[8,8], autosize_y=True):
                with dpg.group(horizontal=True):
                    dpg.add_button(label='Открыть файл', width=94, height=50, tag='open', pos=[1,4],callback=lambda: dpg.show_item("file_dialog_id"))
                    if os.path.isfile(os.getcwd()+'\\'+'my_db.db'):
                        dpg.configure_item("open", enabled=False)
                        dpg.configure_item("log", color=(0,255,0))
                        dpg.set_value('log','БД уже создана')
                    else:
                        dpg.configure_item("log", color=(255,0,0))
                        dpg.set_value('log','БД не найдена, ... Выберите файл (.*csv)')
                        
                        
                    dpg.add_button(label='Обновить', tag='update',width=94, height=50, callback=lambda: update_db(*dpg.get_values(['name','login','pwd'])))
                    if dpg.get_value('name')=='':
                        dpg.configure_item("update", enabled=False)
                        dpg.configure_item("log", color=(255,0,0))
                        dpg.set_value('log','Нет подключения к БД')
                    else:
                        dpg.configure_item("update", enabled=True)
        dpg.bind_font(font1)
                   
    
                        

if __name__=='__main__':
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("start_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
