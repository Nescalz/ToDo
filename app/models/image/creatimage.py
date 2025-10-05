from requests import get
from asyncio import sleep
from PIL import Image, ImageDraw, ImageFont

from pathlib import Path


root_path = Path(__file__).resolve().parents[1]

async def valuts():
    global data
    while True:
        data = get('https://www.cbr-xml-daily.ru/daily_json.js').json() 
        
        image = Image.open(f"{root_path}\\image\\default_valuts.jpg")
        font = ImageFont.truetype("tahoma.ttf", 50)
        drawer = ImageDraw.Draw(image)
        drawer.text((180, 130), f"$ {data['Valute']['USD']['Value']}\n¥ {data['Valute']['CNY']['Value']}\nDH {data['Valute']['AED']['Value']}", font=font, fill='black')

        image.save(f"{root_path}\\image\\new_valuts.jpg")
        await sleep(86400)
        