from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from misc import messages
from keyboards.inline import admin
from services.orders import check_order, get_order
from states import AdminBotStates, BotStates
from services.admin import extend_user_sub, end_user_sub, set_discount, test
from services.actions import rebuild_server_config


async def admin_start_handler(message : types.Message):
    """Главное меню администратора"""
    if message.from_user.id in message.bot.get('config').tg_bot.admin_ids:
        await message.answer(
            messages.ADMIN_HELLO,
            parse_mode='Markdown',
            reply_markup=admin.admin_start_keyboard()
        )

async def admin_start(callback : types.CallbackQuery):
    """Главное меню администратора"""
    if callback.from_user.id in callback.bot.get('config').tg_bot.admin_ids:
        await callback.message.edit_text(
            messages.ADMIN_HELLO,
            parse_mode='Markdown',
            reply_markup=admin.admin_start_keyboard()
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
                    reply_markup=admin.back_admin_start_keyboard()
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
                    reply_markup=admin.back_admin_start_keyboard()
                    )
            await BotStates.MAIN.set()
        else:
            await message.answer(
                    messages.ADMIN_ORDER_NOT_EXIST,
                    parse_mode='Markdown',
                    reply_markup=admin.back_admin_start_keyboard()
                    )
            await BotStates.MAIN.set()


async def admin_enter_user_id(callback: types.CallbackQuery, state: FSMContext):
    """Ввод user_id для изменения подписки"""
    if callback.from_user.id in callback.bot.get('config').tg_bot.admin_ids:
        await callback.message.edit_text(messages.ADMIN_ENTER_USER_ID)
        await AdminBotStates.USER_ID_SUB.set()

async def admin_actions_sub(message : types.Message, state: FSMContext):
    if message.from_user.id in message.bot.get('config').tg_bot.admin_ids:
        try:
            user_id = int(message.text)
        except:
            await message.answer(
                messages.ADMIN_INT_ERROR,
                parse_mode='Markdown',
                reply_markup=admin.back_admin_start_keyboard()
            )
            await BotStates.MAIN.set()
            return
        await state.update_data(edit_user_id=user_id)
        await message.answer(
                messages.ADMIN_USER_ACTIONS,
                parse_mode='Markdown',
                reply_markup=admin.admin_user_sub_keyboard()
            )
        await BotStates.MAIN.set()

async def admin_extend_sub_enter_days(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in callback.bot.get('config').tg_bot.admin_ids:
        await callback.message.edit_text(messages.ADMIN_ENTER_SUB_DAYS)
        await AdminBotStates.DAYS_EXTEND.set()

async def admin_extend_sub(message: types.Message, state: FSMContext):
    if message.from_user.id in message.bot.get('config').tg_bot.admin_ids:
        try:
            sub_days = int(message.text)
        except:
            await message.answer(
                messages.ADMIN_INT_ERROR,
                parse_mode='Markdown',
                reply_markup=admin.back_admin_start_keyboard()
            )
            await BotStates.MAIN.set()
            return
        data = await state.get_data()
        edit_user_id = data.get('edit_user_id')
        await extend_user_sub(edit_user_id, sub_days)
        await message.answer(messages.ADMIN_SUB_UPDATED.format(id=edit_user_id),
                            reply_markup=admin.back_admin_start_keyboard())
        await BotStates.MAIN.set()

async def admin_end_sub(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in callback.bot.get('config').tg_bot.admin_ids:
        await callback.answer()

async def admin_set_discount(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in callback.bot.get('config').tg_bot.admin_ids:
        await callback.message.edit_text(messages.ADMIN_ENTER_DISCOUNT)
        await AdminBotStates.SET_DISCOUNT.set()

async def admin_discount(message: types.Message, state: FSMContext):
    if message.from_user.id in message.bot.get('config').tg_bot.admin_ids:
        try:
            user_id, discount = map(int, message.text.split())
        except:
            await message.answer(
                messages.ADMIN_INT_ERROR,
                parse_mode='Markdown',
                reply_markup=admin.back_admin_start_keyboard()
            )
            await BotStates.MAIN.set()
            return
        await set_discount(user_id, discount)
        await message.answer(messages.ADMIN_SUB_UPDATED.format(id=user_id, discount=discount),
                            reply_markup=admin.back_admin_start_keyboard())
        await BotStates.MAIN.set()

async def admin_rebuild_server_config(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in callback.bot.get('config').tg_bot.admin_ids:
        await callback.answer()
        await callback.message.answer(messages.ADMIN_START_REBUILD_SERVER_CONF)
        await rebuild_server_config()

async def admin_test_btn(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in callback.bot.get('config').tg_bot.admin_ids:
        # test()
        await callback.answer()





def register_admin_handlers(dp : Dispatcher):
    dp.register_message_handler(admin_start_handler, commands=['iamobiwan'], state='*')
    dp.register_message_handler(admin_check_order, state=AdminBotStates.ORDER_ID)
    dp.register_message_handler(admin_actions_sub, state=AdminBotStates.USER_ID_SUB)
    dp.register_message_handler(admin_extend_sub, state=AdminBotStates.DAYS_EXTEND)
    dp.register_message_handler(admin_discount, state=AdminBotStates.SET_DISCOUNT)
    dp.register_callback_query_handler(admin_enter_order_id, text='admin_enter_order_id', state='*')
    dp.register_callback_query_handler(admin_start, text='back_admin_menu', state='*')
    dp.register_callback_query_handler(admin_enter_user_id, text='admin_manage_sub', state='*')
    dp.register_callback_query_handler(admin_extend_sub_enter_days, text='admin_extend_sub', state='*')
    dp.register_callback_query_handler(admin_end_sub, text='admin_end_sub', state='*')
    dp.register_callback_query_handler(admin_set_discount, text='admin_set_discount', state='*')
    dp.register_callback_query_handler(admin_rebuild_server_config, text='admin_rebuild_server_config', state='*')
    dp.register_callback_query_handler(admin_test_btn, text='admin_test', state='*')