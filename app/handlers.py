from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiosqlite import connect

import re

from json import loads

import app.keyboards as kb
import app.config as cfg
import app.models.database as db
import app.models.image.creatimage as image
import app.models.cleasure as func_data

import app.models.dictionary as dict_func
router = Router()

add_data, give_data = func_data.conteiner()

has_special = re.compile("|".join(map(re.escape, ".,:;!_*-+()/#¤%&)"))).search

class Add_text(StatesGroup):
    number_text = State()
    name = State()
    text = State()

class Add_dir(StatesGroup):
    name = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    photo = FSInputFile(f"{image.root_path}\\image\\new_valuts.jpg")
    await message.answer_photo(caption="Доброго времени суток!\nЦены выше представлены к Рублю", photo=photo)
    await message.answer(text="Меню", reply_markup=kb.start_menu)

@router.callback_query(F.data == "notes")
async def message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    id_user = callback.from_user.id

    result = loads(await db.jsons(id_user)) #Превращяем список из бд в JSON  

    keyb = await kb.json_one(result, None) #Делаем кнопки по JSON разметке

    result = dict_func.build_paths(result)

    await callback.message.edit_text(f"Ваши папки и заметки.\n{result}", reply_markup=keyb)

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
    keyb = await kb.json_one(data, f'dir{number_text}')

    await callback.message.edit_text(f"{data}", reply_markup=keyb) 

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
    keyb = await kb.json_one(data, f"dir{number_text}")
    
    await callback.message.edit_text(f"{data}", reply_markup=keyb)

@router.callback_query(F.data.startswith("edit_"))
async def message(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    user_id = callback.from_user.id
    number_text = callback.data.split("_")[1]

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

@router.callback_query(F.data == "no")
async def message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    number_text = callback.data.split("_")[1]
    number_type = callback.data.split("_")[2]
    user_id = callback.from_user.id
    data = loads(await db.jsons(user_id))

    if number_type == "text":
        keyb, text = await kb.text_view(data, f"{number_text}")
    elif number_type == "dir":
        text = ""
        keyb = await kb.json_one(data, f'dir{number_text}')

    await callback.message.edit_text(text, reply_markup=keyb)

@router.callback_query(F.data == "yes")
async def message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    number_text = callback.data.split("_")[1]
    number_type = callback.data.split("_")[2]
    user_id = callback.from_user.id
    data = loads(await db.jsons(user_id))


    new_data = dict_func.remove_by_type_index(data, number_text, number_type)
    number_text = dict_func.find_parent_index(data, number_text, number_type)

    await db.new_data_reset(user_id, new_data)
    keyb = await kb.json_one(data, f'dir{number_text}') #dir, потому что всегда тип прошлой структуры равен папке
    await callback.message.edit_text("text", reply_markup=keyb) #text - заглушка


@router.callback_query(F.data.startswith("add_"))
async def message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    number_type = callback.data.split("_")[1]
    number_text = callback.data.split("_")[2]
    await state.update_data(number_text=number_text)
    if number_type == "text": 
        await callback.message.edit_text("Введите название заметки", reply_markup=kb.cancel(number_text))
    elif number_type == "dir":
        await callback.message.edit_text("Введите название папки", reply_markup=kb.cancel(number_text))
    await state.set_state(Add_dir.name)
    add_data(user_id, number_text)

@router.callback_query(Add_text.name)
async def message(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Add_text.text)
    user_id = message.from_user.id
    number_text = give_data(user_id)
    await message.answer("Что хотите записать в заметку?\nВы можете использовать все символы кроме специальных символов и скобок.", reply_markup=kb.cancel(number_text)) 

@router.callback_query(Add_dir.name) 
async def message(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    number_text = give_data(user_id)
    data = loads(await db.jsons(user_id))

    await state.clear()
    data, index = dict_func.add_to_folder(data, number_text, "dir", message.text) #Сдеалть экранирование текста
    await db.new_data_reset(user_id, data)
    await message.answer("", reply_markup=kb.json_one(data, f'dir{index}')) 
    

@router.callback_query(Add_text.text)
async def message(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    number_text = give_data(user_id)
    data = loads(await db.jsons(user_id))

    await state.clear()
    data, index = dict_func.add_to_folder(data, number_text, "text", await state.get_data["name"], message.text)
    await db.new_data_reset(user_id, data)
    kb.text_view(data, f'{index}')
    await message.answer(message.text, reply_markup=kb.json_one(data, f'text{index}')) 