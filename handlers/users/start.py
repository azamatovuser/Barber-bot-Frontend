import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from states.ClientInfoState import ClientInfoState
from data.config import BASE_URL


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, Ismingizni kiriting 👇")
    await ClientInfoState.first_name.set()


@dp.message_handler(state=ClientInfoState.first_name)
async def first(message:types.Message, state: FSMContext):
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
    await message.answer(f"Raqamingizni kiriting 👇")
    await ClientInfoState.number.set()


@dp.message_handler(state=ClientInfoState.number)
async def numb(message:types.Message, state: FSMContext):
    await state.update_data(
        {"number": message}
    )
    data = await state.get_data()
    requests.post(url=f"{BASE_URL}main/create/", data=data)
    await message.answer(f"Success!")
    await state.finish()