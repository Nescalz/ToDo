from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import app.models.dictionary as dict_func

main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить заявку", callback_data="cancel")]])

start_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Заметки", callback_data="notes")], 
                                              [InlineKeyboardButton(text="Задачи", callback_data="tasks")],
                                              [InlineKeyboardButton(text="Настройка", callback_data="settings")]])


async def json_one(data, number_text):
    
    data_default = data
    keyb = [[InlineKeyboardButton(text="📂 Добавить папку", callback_data="add_dirs")],
            [InlineKeyboardButton(text="📔 Добавить заметку", callback_data="add_txt")]]
    if number_text == None:
        pass
    elif number_text.startswith("dir"):
        number_text = number_text[3:]
        data = dict_func.find_index(data, number_text, "dir")

    elif number_text.startswith("text"):
        number_text = number_text[4:]
        data = dict_func.find_index(data, number_text, "text")

    print(data)
    data_key = next(iter(data))
    data = data[data_key]

    


    dir={}
    file={}
        
    for i in data.items():
        if i[0].startswith("dir"):
            key = i[0].split("_", maxsplit=1)[0][3:]
            name = i[0].split("_", maxsplit=1)[1]
            dir[key] = name

        elif i[0].startswith("text"):
            key = i[0].split("_", maxsplit=1)[0][4:]
            name = i[0].split("_", maxsplit=1)[1]
            file[key] = name

    for k, v in dir.items():
        keyb.append([InlineKeyboardButton(text=f"📂 {v}", callback_data=f"dir{k}")])

    for k, v in file.items():
        keyb.append([InlineKeyboardButton(text=f"📔 {v}", callback_data=f"text{k}")])

    keyb.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_{number_text}")])

    keybord = InlineKeyboardMarkup(inline_keyboard=keyb) #Список с файлами и папками
    return keybord