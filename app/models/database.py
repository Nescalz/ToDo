from aiosqlite import connect

async def jsons(user_id):
    async with connect("database.db") as db:
        async with db.execute(
            "SELECT json FROM Users WHERE telegram_id = ?", 
            (user_id,)) as cursor:
                row = await cursor.fetchone()
                return row[0]
        