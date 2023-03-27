from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def start(message : types.Message):
    await message.answer(f'Бот запущен')


async def echo(message : types.Message):
    await message.answer(f'Это эхо сообщение: {message.text}')

def register_user_handlers(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(echo)
