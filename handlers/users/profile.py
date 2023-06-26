from aiogram import types
from loader import dp, bot
import requests
from data.config import BASE_URL, ADMINS
from keyboards.default.main_button import main_button


@dp.message_handler(text="Mening ma'lumotim")
async def profile(message:types.Message):

    client = message.from_user.id
    admin = ADMINS[0]
    if int(client) == int(admin):
        await message.answer("Qanaqa ma'lumot?")
    else:
        back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        back.add('Orqaga qaytish')
        client_id = message.from_user.id
        rs = requests.get(url=f"{BASE_URL}main/client/detail/{client_id}/")
        client = rs.json()
        await message.answer(f"Ism: {client['first_name']}\n"
                             f"Familya: {client['last_name']}\n"
                             f"Raqam: {client['number']}", reply_markup=back)


@dp.message_handler(text="Orqaga qaytish")
async def profile(message:types.Message):

    client = message.from_user.id
    admin = ADMINS[0]
    if int(client) == int(admin):
        await message.answer("Orqaga qaytish deysizmi?")
    else:
        await message.answer(f"{message.from_user.first_name}", reply_markup=main_button)