from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from keyboards.inline.main import back_main_keyboard
from misc import messages


async def instruction(callback: types.CallbackQuery):
    """ Инструкция для пользователя """
    await callback.message.edit_text(
        messages.INSTRUCTION,
        parse_mode='Markdown',
        disable_web_page_preview=True,
        reply_markup=back_main_keyboard()
    )

async def instruction_handler(message: types.Message):
    """ Инструкция для пользователя """
    await message.answer(
        messages.INSTRUCTION,
        parse_mode='Markdown',
        disable_web_page_preview=True,
        reply_markup=back_main_keyboard()
    )

def register_instruction_handlers(dp : Dispatcher):
    dp.register_message_handler(instruction_handler, commands=['instruction'], state='*')
    dp.register_callback_query_handler(instruction, text='instruction', state='*')
