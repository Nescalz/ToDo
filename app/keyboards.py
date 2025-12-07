from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import app.models.dictionary as dict_func

main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отменить заявку", callback_data="cancel")]])

start_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Заметки", callback_data="notes")], 
                                              [InlineKeyboardButton(text="Задачи", callback_data="tasks")],
                                              [InlineKeyboardButton(text="Настройка", callback_data="settings")]])

def yes_or_no(number_text, type):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Да", callback_data=f"yes_{number_text}_{"text" if type == "text" else "dir"}")], 
                                              [InlineKeyboardButton(text="Нет", callback_data=f"no_{number_text}_{"text" if type == "text" else "dir"}")]])

def back_in_addfolder(number_text):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти в папку", callback_data=f"cancel_{number_text}")]])

def cancel(number_text):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data=f"cancel_{number_text}")]])

async def json_one(data, number_text):
    keyb = [[InlineKeyboardButton(text="📂 Добавить папку", callback_data=f"add_dir_{number_text}")],
            [InlineKeyboardButton(text="📔 Добавить заметку", callback_data=f"add_text_{number_text}")]]
    if number_text == None:
        pass
    elif number_text.startswith("dir"): #Dir - не уникальный интендификатор, служит заглушкой, чтобы было != None
        number_text = number_text[3:]
        data = dict_func.find_index(data, number_text, "dir")

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
        keyb.append([InlineKeyboardButton(text=f"📄 {v}", callback_data=f"text{k}")])

    keyb.append([InlineKeyboardButton(text="🗑 Удалить папку", callback_data=f"deletedir_{number_text}")])
    keyb.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_{number_text}_dir")])

    keybord = InlineKeyboardMarkup(inline_keyboard=keyb) 
    return keybord

async def text_view(data, number_text):
    data = dict_func.find_index(data, number_text, "text")

    data_key = next(iter(data))
    text = data[data_key]

    keyb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Редактировать", callback_data=f"edit_{number_text}")],
            [InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_{number_text}")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_{number_text}_text")]
            ])
    return keyb, text