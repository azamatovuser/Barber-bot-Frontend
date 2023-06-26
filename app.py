from aiogram import executor

from loader import dp, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    # await bot.set_webhook(url='https://relaxbro.pythonanywhere.com')


if __name__ == '__main__':
    # executor.start_webhook(dp, on_startup=on_startup, webhook_path='/', host='relaxbro.pythonanywhere.com', port=80)
    executor.start_polling(dp, on_startup=on_startup)
