from aiosqlite import connect
import json

async def jsons(user_id):
    async with connect("database.db") as db:
        async with db.execute(
            "SELECT json FROM Users WHERE telegram_id = ?", 
            (user_id,)) as cursor:
                row = await cursor.fetchone()

                if row is None:
                    empty_json = json.dumps({'dir0_main': {}}, ensure_ascii=False)
                    await db.execute(
                        "INSERT INTO Users (telegram_id, json) VALUES (?, ?)",
                        (user_id, empty_json)
                    )
                    await db.commit()
                    
                    return empty_json
                return row[0]
        
async def new_data_reset(user_id, data):
    async with connect("database.db") as db:
        jsons = json.dumps(data, ensure_ascii=False)
        await db.execute("UPDATE Users SET json = ? WHERE telegram_id = ?", (jsons, user_id,))
        await db.commit()