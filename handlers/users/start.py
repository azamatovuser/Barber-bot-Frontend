import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from states.ClientInfoState import ClientInfoState
from data.config import BASE_URL, ADMINS
from keyboards.default.main_button import main_button
from keyboards.default.schedule_button import schedule_button


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    rs = requests.get(url=f"{BASE_URL}main/list/")
    data = rs.json()
    client = message.from_user.id
    admin = ADMINS[0]
    if int(client) == int(admin):
        await message.answer('Ish jadvali', reply_markup=schedule_button)
    else:
        clients = []
        for i in data:
            clients.append(i['telegram_id'])
        if client in clients:
            await message.answer(f"{message.from_user.first_name}", reply_markup=main_button)
        else:
            print('Qayerga ketding?')
            await message.answer(f"Salom, Ismingizni kiriting 👇", reply_markup=types.ReplyKeyboardRemove())
            await ClientInfoState.first_name.set()


@dp.message_handler(state=ClientInfoState.first_name)
async def first(message:types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    await state.update_data(
        {"telegram_id": telegram_id}
    )
    await state.update_data(
        {"first_name": message}
    )
    await message.answer(f"Familyangizni kiriting 👇")
    await ClientInfoState.last_name.set()


@dp.message_handler(state=ClientInfoState.last_name)
async def last(message:types.Message, state: FSMContext):
    await state.update_data(
        {"last_name": message}
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(text="Contact", request_contact=True))
    await message.answer(f"Raqamingizni kiriting 👇", reply_markup=markup)
    await ClientInfoState.number.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=ClientInfoState.number)
async def numb(message:types.Message, state: FSMContext):
    contact = message.contact
    phone_number = contact.phone_number
    await state.update_data(
        {"number": '+' + phone_number}
    )
    data = await state.get_data()
    requests.post(url=f"{BASE_URL}main/create/", data=data)
    await message.answer(f"{message.from_user.first_name}", reply_markup=main_button)
    await state.finish()