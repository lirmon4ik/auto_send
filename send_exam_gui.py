# -*- coding: cp1251 -*-

import dearpygui.dearpygui as dpg
from win32api import GetSystemMetrics


dpg.create_context()
 
with dpg.font_registry():
	with dpg.font("NotoMono-Regular.ttf", 12, default_font=True) as font1:

		# add the default font range
		dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)

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


list_log=[]
list_output=[]

def ret_value(sender, data):
    items = dpg.get_item_configuration("lb_2")['items']
    items.append(data)
    dpg.configure_item("lb_2", items=items)

    
    items = dpg.get_item_configuration("lb_1")['items']
    print(type(items))
    items.remove(data)
    dpg.configure_item("lb_1", items=items)

    list_log.append(f"Добавлен обьект {data} в lb_2 ")
    list_log.append(f"Убран обьект {data} из lb_1 ")

    dpg.set_value('log', ''.join(list_log))
    




dpg.create_viewport(title='Custom Title', 
                    width=int(width/2), 
                    height=int(height/2),
                    min_width=int(width/2),
                    min_height=int(height/2),
                    x_pos=int(width/4),
                    y_pos=int(height/4),
                    max_width=int(width/2),
                    max_height=int(height/2))


with dpg.window(tag="start_window"):
        dpg.add_listbox(items=['неустроев сергей','долгов дима'], 
                        tag='lb_1', 
                        callback=ret_value,
                        width=205,
                        pos=[535,14],
                        num_items=21
                        )
        dpg.add_listbox(items=[],
                        tag='lb_2',
                        width=205,
                        pos=[320,14],
                        num_items=21
                        )
        with dpg.child_window(width=300, pos=[8,10], height=270):
            dpg.add_text(tag='text_output',wrap=1)
        with dpg.child_window(width=300, pos=[8,290], autosize_y=True):
            dpg.add_text(tag='log',wrap=250)
        dpg.bind_font(font1)
            
        
            
    
                        


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("start_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
