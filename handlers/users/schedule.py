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

rs = requests.get(url=f"{BASE_URL}main/schedule/create/")
data = rs.json()
available_times = [f"{i['month']} {i['day']} {i['time']}" for i in data]


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


@dp.message_handler()
async def handle_selected_time(message: types.Message):
    selected_time = message.text
    parts = selected_time.split()
    month = parts[0]
    day = int(parts[1])
    time = parts[2]
    user_id = message.from_user.id
    if selected_time in available_times:
        response = requests.put(url=f"{BASE_URL}main/schedule/update/", data={
            'month': month,
            'day': day,
            'time': time,
            'user_id': user_id
        })
        await message.reply(f"You have selected: {selected_time}")
    else:
        await message.reply("Invalid selection. Please choose an available time.")