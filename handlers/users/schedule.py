from aiogram import types
from loader import dp, bot
from data.config import BASE_URL, ADMINS
from states.ScheduleSetInfo import ScheduleSetInfo
from aiogram.dispatcher import FSMContext
from keyboards.default.schedule_button import schedule_button
from keyboards.default.available_time import available_time
from keyboards.default.main_button import main_button
import datetime
import requests


@dp.message_handler(text="Vaqt belgilash")
async def schedule(message: types.Message):
    client = message.from_user.id
    admin = ADMINS[0]
    if int(client) != int(admin):
        await message.answer('Vaqt belgilash deysizmi?')
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.add('Bekor qilish')
    await message.answer('Qaysi kunga bergilap bermoqchisiz?', reply_markup=menu)
    await ScheduleSetInfo.day.set()


@dp.message_handler(state=ScheduleSetInfo.day)
async def day_set(message: types.Message, state: FSMContext):
    if message.text == 'Bekor qilish':
        await state.finish()
        await message.reply("Bekor qilindi", reply_markup=schedule_button)
    else:
        month = datetime.datetime.now().strftime('%B')
        day = message
        await state.update_data(
            {
                "month": month,
                "day": day
            }
        )
        await message.answer('Qaysi vaqtga bergilap bermoqchisiz?')
        await ScheduleSetInfo.time.set()


@dp.message_handler(state=ScheduleSetInfo.time)
async def time_set(message: types.Message, state: FSMContext):
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


@dp.message_handler(text="Yozdirib qo'yish")
async def set_time(message: types.Message):
    await message.answer("Sizga qaysi vaqt qulay?", reply_markup=available_time)


@dp.message_handler(text="Bekor qilish")
async def set_time(message: types.Message):
    await message.answer(f"{message.from_user.first_name}", reply_markup=main_button)


print(available_time.keyboard)


@dp.message_handler(lambda message: message.text in available_time.keyboard)
async def handle_dynamic_message(message: types.Message):
    selected_time = message
    await message.answer(f"Siz shu vaqtni tanladiz - {selected_time}", reply_markup=types.ReplyKeyboardRemove())