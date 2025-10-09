from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from app.database.database import jsons

from json import loads
main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить заявку", callback_data="cancel")]])

start_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Заметки", callback_data="notes")], 
                                              [InlineKeyboardButton(text="Задачи", callback_data="tasks")],
                                              [InlineKeyboardButton(text="Настройка", callback_data="settings")]])


async def json_one(data, save_data, id_user, number_text):
    data_clear = data
    keyb = [[InlineKeyboardButton(text="📂 Добавить папку", callback_data="add_dirs")],
            [InlineKeyboardButton(text="📔 Добавить заметку", callback_data="add_txt")]]
    dir = []
    file = []
    button_for_index = {}
    x = 0
    y = 0
    
    if number_text != None:
        if number_text.startswith("dir_"):
            print(data)
            
        elif number_text.startswith("text_"):
            return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_")]]), data[f'{number_text}']
        
    for i in data.items():
        if i[0].startswith("dir_"):
            dir.append(i[0])
            button_for_index[f"dir_{list(i.items)[0]}"] = i
            x += 1

        elif i[0].startswith("text_"):
            file.append(i[0])
            button_for_index[f"text_{i[0]}"] = i   
            y += 1     


    save_data(id_user, button_for_index)

    for x, i in enumerate(dir):
        keyb.append([InlineKeyboardButton(text=f"📂 {i[4:]}", callback_data=f"dir_{x}")])

    for x, i in enumerate(file):
        keyb.append([InlineKeyboardButton(text=f"📔 {i[5:]}", callback_data=f"text_{x}")])

    print(data_clear)
    keyb.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_{number_text}")])

    keybord = InlineKeyboardMarkup(inline_keyboard=keyb) #Список с файлами и папками
    return keybord