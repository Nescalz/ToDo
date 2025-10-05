import asyncio
from aiogram import Bot, Dispatcher, F
from sqlite3 import connect
from app.config import token

from app.handlers import router
from app.models.image.creatimage import valuts

connectdb = connect("database.db")
cursor = connectdb.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    json TEXT
)
''')


async def main():
    asyncio.create_task(valuts()) 
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("off")
