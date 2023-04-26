from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.main import back_main_keyboard
from services.vpn import generate_vpn_settings, send_vpn_settings, change_vpn_status_to_requested
from db.models import User, Vpn
from misc import messages
from loader import logger
from datetime import datetime



async def get_vpn(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    vpn_status = user_data.get('vpn_status')
    if user_data.get('status') in ['trial', 'subscribed']:
        if vpn_status == 'created':
            await change_vpn_status_to_requested(state, user_data.get('id'))
            await callback.message.edit_text(
            messages.REQUEST_FOR_VPN,
            parse_mode='Markdown',
            reply_markup=back_main_keyboard()
            )
        elif vpn_status == 'pending':
            await callback.message.edit_text(
            messages.WAIT_FOR_SETTINGS,
            parse_mode='Markdown',
            reply_markup=back_main_keyboard()
        )
        elif vpn_status == 'executed':
            await send_vpn_settings(user_data)
    else:
        await callback.message.edit_text(
            messages.GET_VPN_UNSUB,
            parse_mode='Markdown',
            reply_markup=back_main_keyboard()
        )

async def get_vpn_handler(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    vpn_status = user_data.get('vpn_status')
    if user_data.get('status') in ['trial', 'subscribed']:
        if vpn_status == 'created':
            await change_vpn_status_to_requested(state, user_data.get('id'))
            await message.answer(
            messages.REQUEST_FOR_VPN,
            parse_mode='Markdown',
            reply_markup=back_main_keyboard()
            )
        elif vpn_status == 'pending':
            await message.answer(
            messages.WAIT_FOR_SETTINGS,
            parse_mode='Markdown',
            reply_markup=back_main_keyboard()
        )
        elif vpn_status == 'executed':
            await send_vpn_settings(user_data)
    else:
        await message.answer(
            messages.GET_VPN_UNSUB,
            parse_mode='Markdown',
            reply_markup=back_main_keyboard()
        )

def register_vpn_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(get_vpn, text='get_vpn', state='*')
    dp.register_message_handler(get_vpn_handler, commands=['getvpn'], state='*')


# async def get_vpn(message : types.Message, user, **kwargs):
#     if user:
#         if user.vpn_status == 'not requested':
#             await message.answer(
#                 f'Мы получили Ваш запрос на формирование настроек.\n\n'\
#                 f'В течение 5 минут бот обработает Ваш запрос и пришлет настройки\n\n'
#                 f'Ожидайте...',
#                 parse_mode='Markdown',
#                 reply_markup=back_main()
#                 )
#             generate_user_config(user)
#         elif user.vpn_status == 'pending':
#             await message.answer(
#                 f'Ваши настройки формируются.\n\n'\
#                 f'В течение 5 минут бот обработает Ваш запрос и пришлет настройки\n\n'
#                 f'Ожидайте...',
#                 parse_mode='Markdown',
#                 reply_markup=back_main()
#                 )
#         else:
#             await send_settings(user)
#     else:
#         await message.answer(
#                 f'Для доступа ко всем функциям бота оформите подписку!\n\n',
#                 parse_mode='Markdown',
#                 reply_markup=unsubscribed_keyboard(user)
#                 )

