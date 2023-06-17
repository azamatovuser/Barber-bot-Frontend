from aiogram import types
from loader import dp, bot
from data.config import BASE_URL, ADMINS
from states.ScheduleSetInfo import ScheduleSetInfo
from aiogram.dispatcher import FSMContext
from keyboards.default.schedule_button import schedule_button
import datetime
import requests


@dp.message_handler(text="Vaqt belgilash")
async def schedule(message:types.Message):
    client = message.from_user.id
    admin = ADMINS[0]
    if int(client) != int(admin):
        await message.answer('Vaqt belgilash deysizmi?')
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.add('Bekor qilish')
    await message.answer('Qaysi kunga bergilap bermoqchisiz?', reply_markup=menu)
    await ScheduleSetInfo.day.set()


@dp.message_handler(state=ScheduleSetInfo.day)
async def day_set(message:types.Message, state:FSMContext):
    if message.text == 'Bekor qilish':
        await state.finish()
        await message.reply("Bekor qilindi", reply_markup=schedule_button)
    else:
        client_id = ADMINS[0]
        month = datetime.datetime.now().strftime('%B')
        day = message
        await state.update_data(
            {"user_id": client_id,
             "month": month,
             "day": day
             }
        )
        await message.answer('Qaysi vaqtga bergilap bermoqchisiz?')
        await ScheduleSetInfo.time.set()


@dp.message_handler(state=ScheduleSetInfo.time)
async def time_set(message:types.Message, state:FSMContext):
    if message.text == 'Bekor qilish':
        await state.finish()
        await message.reply("Bekor qilindi", reply_markup=schedule_button)
    else:
        time = message
        await state.update_data(
            {"time": time}
        )
        data = await state.get_data()
        requests.post(url=f"{BASE_URL}main/schedule/create/", data=data)
        await message.answer(f"Ish bitdi", reply_markup=schedule_button)
        await state.finish()