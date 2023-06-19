from aiogram.types import ReplyKeyboardMarkup
from data.config import BASE_URL
import requests

rs = requests.get(url=f"{BASE_URL}main/schedule/create/")
data = rs.json()

available_time = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
for i in data:
    available_time.add(f"{i['month']} {i['day']} {i['time']}")
available_time.add('Bekor qilish')