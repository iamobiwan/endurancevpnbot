from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from handlers.main import main
from keyboards.inline.main import back_main_keyboard
from keyboards.inline.subscribe import back_my_sub_keyboard
from keyboards.inline.promocode import have_promocode_keyboard
from services.promocode import check_promocode, generate_promocode
from states import BotStates
from misc import status, messages
from loader import logger


async def question_promocode(callback: types.CallbackQuery, state: FSMContext):
    """ Вопрос пользователю о наличии промокода """
    await callback.message.edit_text(
            messages.HAVE_PROMOCODE,
            reply_markup=have_promocode_keyboard(callback)
    )

async def have_promocode(callback: types.CallbackQuery):
    """ Ввод промокода """
    await callback.answer()
    await callback.message.edit_text(messages.ENTER_PROMOCODE)
    await BotStates.PROMOCODE.set()

async def enter_promocode(message : types.Message, state: FSMContext):
    """ Проверка введенного промокода """
    user_data = await state.get_data()

    if user_data.get('promocode_used') == 'True':
        await message.edit_text(
            messages.ALREADY_USE_PROMOCODE,
            reply_markup=back_main_keyboard()
        )
    else:
        promocode = message.text
        if await check_promocode(message, state, promocode):
            pass
        else:
            await message.answer(
                messages.NO_PROMOCODE,
                parse_mode='Markdown',
                reply_markup=back_main_keyboard()
                )
            
    await BotStates.MAIN.set()

async def get_promocode(callback: types.CallbackQuery, state: FSMContext):
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
    dp.register_callback_query_handler(question_promocode, regexp=r"(trial|get_sub)", state='*')
    dp.register_callback_query_handler(have_promocode, text='yes_promocode', state='*')
    dp.register_callback_query_handler(get_promocode, text='get_promocode', state='*')