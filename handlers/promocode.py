from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from handlers.main import main
from handlers.subscribe import activate_trial
from keyboards.inline.main import back_main_keyboard
from keyboards.inline.subscribe import back_my_sub_keyboard
from services.promocode import check_promocode, generate_promocode
from states import BotStates
from misc import status, messages
from loader import logger


async def apply_promocode(callback: types.CallbackQuery, state: FSMContext):
    """ Ввод промокода """
    user_data = await state.get_data()
    if user_data.get('promocode_used'):
        await callback.message.edit_text(
            messages.ALREADY_USE_PROMOCODE,
            reply_markup=back_main_keyboard()
        )
    else:
        await callback.message.edit_text(messages.ENTER_PROMOCODE)
        await BotStates.PROMOCODE.set()

async def enter_promocode(message : types.Message, state: FSMContext):
    """ Проверка введенного промокода """
    promocode = message.text

    if await check_promocode(message, state, promocode):
        await message.answer(
            messages.SUCCESS_PROMOCODE,
            parse_mode='Markdown',
            reply_markup=back_main_keyboard()
            )
    else:
        await message.answer(
            messages.NO_PROMOCODE,
            parse_mode='Markdown',
            reply_markup=back_main_keyboard()
            )
        
            
    await BotStates.MAIN.set()

async def get_promocode(callback: types.CallbackQuery, state: FSMContext):
    """ Генерация и вывод промокода пользователю"""
    user_data = await state.get_data()
    if not user_data.get('promocode'):
        promocode = generate_promocode(callback)
        await state.update_data(
            promocode=promocode
        )
    user_data = await state.get_data()
    await callback.message.edit_text(
        messages.APPLY_PROMOCODE.format(code=user_data.get('promocode')),
        parse_mode='Markdown',
        reply_markup=back_my_sub_keyboard()
    )


def register_promocode_handlers(dp : Dispatcher):
    dp.register_message_handler(enter_promocode, state=BotStates.PROMOCODE)
    dp.register_callback_query_handler(apply_promocode, text='get_discount', state='*')
    dp.register_callback_query_handler(get_promocode, text='get_promocode', state='*')