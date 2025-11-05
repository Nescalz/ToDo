from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiosqlite import connect

from json import loads

import app.keyboards as kb
import app.config as cfg
from app.models.database import jsons
import app.models.image.creatimage as image
import app.closure as func

import app.models.dictionary as dict_func
router = Router()

save_data_default, give_data_default, save_data, give_data, add_back_data, give_back_data, remove_back_data = func.make_counter() #Создаем хранилище временных файлов для пользователя

class reg(StatesGroup):
    message = State()
    number = State()
    

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    photo = FSInputFile(f"{image.root_path}\\image\\new_valuts.jpg")
    await message.answer_photo(caption="Доброго времени суток!\nЦены выше представлены к Рублю", photo=photo)
    await message.answer(text="Меню", reply_markup=kb.start_menu)

@router.callback_query(F.data == "notes")
async def message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    id_user = callback.from_user.id

    result = loads(await jsons(id_user)) #Превращяем список из бд в JSON

    save_data_default(id_user, result) #Сохраняем изначальный путь

    keyb = await kb.json_one(result, None) #Делаем кнопки по JSON разметке

    result = dict_func.build_paths(result)

    await callback.message.edit_text(f"Ваши папки и заметки.\n{result}", reply_markup=keyb)

@router.callback_query(F.data.startswith("text"))
async def message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    number_text = callback.data[4:]
    data = loads(await jsons(user_id))

    keyb, text = await kb.text_view(data, f"{number_text}")

    await callback.message.edit_text(f"{text}", reply_markup=keyb) 
 
@router.callback_query(F.data.startswith("dir"))
async def message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    number_text = callback.data.split("_", maxsplit=1)[0][3:]
    
    data = loads(await jsons(user_id))
    keyb = await kb.json_one(data, f'dir{number_text}')

    await callback.message.edit_text(f"{data}", reply_markup=keyb) 

@router.callback_query(F.data.startswith("back_"))
async def message(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    user_id = callback.from_user.id
    number_text = callback.data.split("_")[1]
    data = loads(await jsons(user_id))
    if callback.data.split("_")[2] == "text":
        number_text = dict_func.find_parent_index(data, number_text, "text")
    else:
        number_text = dict_func.find_parent_index(data, number_text, "dir")
    keyb = await kb.json_one(data, f"dir{number_text}")
    
    await callback.message.edit_text(f"{data}", reply_markup=keyb)

