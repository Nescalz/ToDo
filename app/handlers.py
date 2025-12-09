from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import re

from json import loads

import app.keyboards as kb
import app.models.database as db
import app.models.cleasure as func_data

import app.models.dictionary as dict_func
router = Router()

add_data, give_data = func_data.conteiner()

has_special = re.compile("|".join(map(re.escape, ".,:;!_*-+()/#¤%&)"))).search

class Add_text(StatesGroup):
    name = State()
    text = State()

class Add_dir(StatesGroup):
    name = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(text="Меню", reply_markup=kb.start_menu)

@router.callback_query(F.data == "notes")
async def message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    id_user = callback.from_user.id
    number_text = "dir0"
    data = loads(await db.jsons(id_user)) #Превращяем список из бд в JSON  

    keyb = kb.json_one(data, number_text) #Делаем кнопки по JSON разметке

    await callback.message.edit_text(f"Ваши папки и заметки.\n{" -> ".join(dict_func.get_folder_path(data, number_text))}", reply_markup=keyb)

@router.callback_query(F.data.startswith("text"))
async def message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    number_text = callback.data[4:]
    data = loads(await db.jsons(user_id))

    keyb, text = await kb.text_view(data, f"{number_text}")

    await callback.message.edit_text(f"{text}", reply_markup=keyb) 
 
@router.callback_query(F.data.startswith("dir"))
async def message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    number_text = callback.data.split("_", maxsplit=1)[0][3:]
    
    data = loads(await db.jsons(user_id))
    keyb = kb.json_one(data, f'dir{number_text}')


    await callback.message.edit_text(f"{" -> ".join(dict_func.get_folder_path(data, int(number_text)))}", reply_markup=keyb) 

@router.callback_query(F.data.startswith("back_"))
async def message(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    user_id = callback.from_user.id
    number_text = callback.data.split("_")[1]
    data = loads(await db.jsons(user_id))
    if callback.data.split("_")[2] == "text":
        number_text = dict_func.find_parent_index(data, number_text, "text")
    else:
        number_text = dict_func.find_parent_index(data, number_text, "dir")
    keyb = kb.json_one(data, f"dir{number_text}")
    
    await callback.message.edit_text(f"{" -> ".join(dict_func.get_folder_path(data, int(number_text)))}", reply_markup=keyb)

#В код ревью стоит объеденить delete и deletedir в один слушатель
@router.callback_query(F.data.startswith("delete_"))
async def message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    number_text = callback.data.split("_")[1]
    await callback.message.edit_text(f"*Вы уверены?*\nДанные о тексте восстановить не получится!", reply_markup=kb.yes_or_no(number_text, "text"), parse_mode="MarkDown")

@router.callback_query(F.data.startswith("deletedir_"))
async def message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    number_text = callback.data.split("_")[1]
    await callback.message.edit_text(f"*Вы уверены?*\nДанные и текста в папке полностью будут удалены!", reply_markup=kb.yes_or_no(number_text, "dir"), parse_mode="MarkDown")

@router.callback_query(F.data.startswith("no_"))
async def message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    number_text = callback.data.split("_")[1]
    number_type = callback.data.split("_")[2]
    user_id = callback.from_user.id
    data = loads(await db.jsons(user_id))

    if number_type == "text":
        keyb, text = await kb.text_view(data, f"{number_text}")
    elif number_type == "dir":
        text = f"{" -> ".join(dict_func.get_folder_path(data, int(number_text)))}"
        keyb = kb.json_one(data, f'dir{number_text}')

    await callback.message.edit_text(text, reply_markup=keyb)

@router.callback_query(F.data.startswith("yes_"))
async def message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    number_text = callback.data.split("_")[1]
    number_type = callback.data.split("_")[2]
    user_id = callback.from_user.id
    data = loads(await db.jsons(user_id))

    number_text2 = dict_func.find_parent_index(data, number_text, number_type)
    new_data = dict_func.remove_by_type_index(data, number_text, number_type)
    await db.new_data_reset(user_id, new_data)
    

    keyb = kb.json_one(new_data, f'dir{number_text2}') #dir, потому что всегда тип прошлой структуры равен папке
    await callback.message.edit_text(f"{" -> ".join(dict_func.get_folder_path(data, int(number_text2)))}", reply_markup=keyb) #text - заглушка


@router.callback_query(F.data.startswith("add_"))
async def message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    number_type = callback.data.split("_")[1]
    number_text = callback.data.split("_")[2]
    add_data(user_id, number_text)
    await state.update_data(number_text=number_text)
    if number_type == "text": 
        await state.set_state(Add_text.name)
        await callback.message.edit_text("Введите название заметки", reply_markup=kb.cancel(number_text))
    elif number_type == "dir":
        await state.set_state(Add_dir.name)
        await callback.message.edit_text("Введите название папки", reply_markup=kb.cancel(number_text))
        

@router.message(Add_text.name)
async def message(message: Message, bot: Bot, state: FSMContext):
    print(1)
    await state.update_data(name=message.text)
    user_id = message.from_user.id
    number_text = give_data(user_id)
    await message.answer("Что хотите записать в заметку?\nВы можете использовать все символы кроме специальных символов и скобок.", reply_markup=kb.cancel(number_text)) 
    await state.set_state(Add_text.text)

@router.message(Add_dir.name) 
async def message(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    number_text = give_data(user_id)
    data = loads(await db.jsons(user_id))
    print(data)
    data, index = dict_func.add_to_folder(data, number_text, "dir", message.text) #Сдеалть экранирование текста
    await db.new_data_reset(user_id, data)
    await message.answer(f"{" -> ".join(dict_func.get_folder_path(data, int(index)))}", reply_markup=kb.json_one(data, f'dir{index}')) 
    await state.clear()
    
@router.message(Add_text.text)
async def message(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    number_text = give_data(user_id)
    data = loads(await db.jsons(user_id))
    data_state = await state.get_data()

    await state.clear()
    data, index = dict_func.add_to_folder(data, number_text, "text", data_state.get("name"), message.text)
    await db.new_data_reset(user_id, data)
    
    await message.answer(message.text, reply_markup=kb.text_view(data, f'{index}')) 

@router.callback_query(F.data.startswith("cancel_"))
async def message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    number_text = callback.data.split("_")[1]
    data = loads(await db.jsons(user_id))
    state.clear()
    await callback.message.edit_text(f"{" -> ".join(dict_func.get_folder_path(data, int(number_text)))}", reply_markup=kb.json_one(data, number_text)) 
