from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from keyboards.inline.main import back_main_keyboard
from misc import messages

async def support(message: types.Message, state: FSMContext):
    """ Главное меню (обработка c message handler)"""
    await message.answer(
        messages.SUPPORT,
        parse_mode='Markdown',
        reply_markup=back_main_keyboard())

def register_support_handlers(dp : Dispatcher):
    dp.register_message_handler(support, commands=['support'], state='*')