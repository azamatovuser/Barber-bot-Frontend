from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ScheduleSetInfo(StatesGroup):
    day = State()
    time = State()