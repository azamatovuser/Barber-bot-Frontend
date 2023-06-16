from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ClientInfoState(StatesGroup):
    first_name = State()
    last_name = State()
    number = State()