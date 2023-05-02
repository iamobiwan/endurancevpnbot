from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from misc import messages
from keyboards.inline.admin import admin_start_keyboard, back_admin_start_keyboard
from services.orders import check_order, get_order
from states import AdminBotStates, BotStates


async def admin_start_handler(message : types.Message):
    """Главное меню администратора"""
    if message.from_user.id in message.bot.get('config').tg_bot.admin_ids:
        await message.answer(
            messages.ADMIN_HELLO,
            parse_mode='Markdown',
            reply_markup=admin_start_keyboard()
        )

async def admin_start(callback : types.CallbackQuery):
    """Главное меню администратора"""
    if callback.from_user.id in callback.bot.get('config').tg_bot.admin_ids:
        await callback.message.edit_text(
            messages.ADMIN_HELLO,
            parse_mode='Markdown',
            reply_markup=admin_start_keyboard()
        )

async def admin_enter_order_id(callback: types.CallbackQuery, state: FSMContext):
    """Ввод order_id"""
    if callback.from_user.id in callback.bot.get('config').tg_bot.admin_ids:
        await callback.message.edit_text(messages.ADMIN_ENTER_ORDER_ID)
        await AdminBotStates.ORDER_ID.set()

async def admin_check_order(message : types.Message, state: FSMContext):
    """Проверка счета и вывод информации о нем"""
    if message.from_user.id in message.bot.get('config').tg_bot.admin_ids:
        try:
            order_id = int(message.text)
        except ValueError:
            await message.answer(
                    messages.ADMIN_INT_ERROR,
                    parse_mode='Markdown',
                    reply_markup=back_admin_start_keyboard()
                    )
            await BotStates.MAIN.set()
            return
        order = get_order(order_id)
        if order:
            if check_order(order):
                status = 'ОПЛАЧЕН'
            else:
                status = 'НЕ ОПЛАЧЕН'
            await message.answer(
                    messages.ADMIN_CHECK_ORDER.format(
                        id=order.id,
                        date=order.created_at.strftime("%d.%m.%Y"),
                        status=status
                    ),
                    parse_mode='Markdown',
                    reply_markup=back_admin_start_keyboard()
                    )
            await BotStates.MAIN.set()
        else:
            await message.answer(
                    messages.ADMIN_ORDER_NOT_EXIST,
                    parse_mode='Markdown',
                    reply_markup=back_admin_start_keyboard()
                    )
            await BotStates.MAIN.set()


def register_admin_handlers(dp : Dispatcher):
    dp.register_message_handler(admin_start_handler, commands=['iamobiwan'], state='*')
    dp.register_message_handler(admin_check_order, state=AdminBotStates.ORDER_ID)
    dp.register_callback_query_handler(admin_enter_order_id, text='admin_enter_order_id', state='*')
    dp.register_callback_query_handler(admin_start, text='back_admin_menu', state='*')