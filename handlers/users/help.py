from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "@azamatovhere ga murojat qiling agar muammolar bo'lsa"
    await message.answer(text=text)
