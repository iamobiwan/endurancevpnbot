from aiogram.dispatcher import FSMContext
from db.models import Server, User
from datetime import datetime, timedelta
from loader import bot, logger, config, dp
from db.connect import session_maker
from db.models import Order, Vpn
from keyboards.inline.main import back_main_keyboard, main_keyboard, expired_user_keyboard
from keyboards.inline.subscribe import my_sub_keyboard
from services.orders import check_order
from services.vpn import generate_vpn_settings, send_vpn_settings, update_server_config
from services.sync import sync_config, check_config
from misc import messages, status
import settings


async def check_pending_orders():
    with session_maker() as session:
        orders = session.query(Order).filter(
            Order.status == 'pending',
            ).all()
        rebuild = False
        if orders:
            for order in orders: # перебор всех заказов
                user_state: FSMContext = dp.current_state(user=order.user.telegram_id, chat=order.user.chat_id) # достаем user_state
                if check_order(order): # проверка оплаты заказа через API y_money
                    rebuild = True
                    logger.info(f'Счет {order.id} успешно оплачен!')
                    user_data = await user_state.get_data()
                    if order.invite_discount: # был ли заказ по чьему-то промокоду?
                        inviting_user = session.query(User).where(User.id == order.user.inviting_user_id).first()
                        if inviting_user.discount >= settings.MAX_DISCOUNT: # у пользователя макс скидка?
                            try:
                                await bot.send_message(
                                chat_id=inviting_user.chat_id,
                                text=messages.MAX_DISCOUNT_FOR_USER,
                                    parse_mode='Markdown',
                                    reply_markup=back_main_keyboard()
                                ) 
                            except:
                                pass
                        else:
                            inviting_user.discount += settings.DISCOUNT_FOR_INVITE_USER
                            try:
                                await bot.send_message(
                                chat_id=inviting_user.chat_id,
                                text=messages.DISCOUNT_FOR_INVITING_USER,
                                    parse_mode='Markdown',
                                    reply_markup=back_main_keyboard()
                                ) 
                            except:
                                pass
                            session.add(inviting_user)
                    order.status = 'success' # обновляем данные заказа и пользователя
                    if order.user.status in ['expired','created', 'outdated']:
                        order.user.expires_at = datetime.now() + timedelta(days=order.days)
                    else:
                        order.user.expires_at += timedelta(days=order.days)
                    order.user.status = 'subscribed'
                    order.user.updated_at = datetime.now()
                    order.updated_at = datetime.now()
                    await user_state.update_data( # обновляем данные в Redis
                        status='subscribed',
                        expires_at=order.user.expires_at.strftime("%d.%m.%Y")
                    )

                    try:
                        await bot.send_message(
                            chat_id=order.user.chat_id,
                            text=messages.SUCCESS_ORDER.format(
                                id=order.id,
                                amount=order.amount,
                                status=status.USER_STATUS.get(order.user.status),
                                expires_at=order.user.expires_at.strftime("%d.%m.%Y")
                            ),
                            parse_mode='Markdown',
                            reply_markup=back_main_keyboard()
                        )
                    except:
                        logger.warning(f'Сообщение об успешной оплате не отправлено пользователю {order.user.id}')

                else: # если заказ не оплачен проверяем, протух ли он
                    diff: timedelta = datetime.now() - order.created_at
                    # if diff.days == settings.ORDER_NOTIFICATION:
                    #     try:
                    #         await bot.send_message(
                    #             chat_id=order.user.telegram_id,
                    #             text=messages.NOTIFY_DELETE_ORDER.format(
                    #                 id=order.id,
                    #                 amount=order.amount,
                    #                 status=order.status
                    #                 )
                    #             )
                    #     except:
                    #         pass
                    if diff.days > settings.PENDING_ORDER_TTL:
                        order.deleted = True
                        order.status = 'expired'
                        order.updated_at = datetime.now()
                        try:
                            await bot.send_message(
                                chat_id=order.user.telegram_id,
                                text=messages.DELETE_ORDER.format(
                                    id=order.id,
                                    amount=order.amount
                                    )
                                )
                        except:
                            pass
                session.add(order)
                session.commit()
            if rebuild:
                await rebuild_server_config()

async def check_pending_vpn():
    with session_maker() as session:
        vpns = session.query(Vpn).filter(Vpn.status == 'pending').all()
        if vpns:
            for vpn in vpns:
                user_state: FSMContext = dp.current_state(user=vpn.user.telegram_id, chat=vpn.user.chat_id)
                user_data = await user_state.get_data()
                try:
                    await generate_vpn_settings(user_state)
                    await send_vpn_settings(user_data)
                except:
                    try:
                        await bot.send_message(
                            chat_id=vpn.user.chat_id,
                            text=messages.GET_SETTING_ERROR,
                            parse_mode='Markdown',
                            reply_markup=back_main_keyboard()
                        )
                    except:
                        pass
                    logger.warning(f'Что-то пошло не так при генерации конфигурации пользователя id={vpn.user_id}')
            await rebuild_server_config()
        else:
            pass

async def rebuild_server_config():
    logger.info('Запускаем обновление конфигурации на серверах...')
    with session_maker() as session:
        servers = session.query(Server).all()
        for server in servers:
            await update_server_config(server)
            await sync_config(server)
            await check_config(server)

async def check_sub_expire():
    logger.info('Запускаем проверку на истечение срока подписки...')
    date = datetime.now()
    with session_maker() as session:
        users = session.query(User).all()
        for user in users:
            user_state: FSMContext = dp.current_state(user=user.telegram_id, chat=user.chat_id)
            user_data = await user_state.get_data()
            if user.status in ['trial', 'subscribed']:
                diff: timedelta = user.expires_at - date
                if date > user.expires_at:
                    logger.info(f'У пользователя {user.id} {user.name} истек срок действия VPN (был {user.status})')
                    user.status = 'expired'
                    user.updated_at = date
                    await user_state.update_data(
                        status = 'expired'
                    )
                    try:
                        await bot.send_message(
                            user.telegram_id,
                            messages.EXPIRED_SUB,
                            reply_markup=expired_user_keyboard()    
                            )
                    except:
                        pass
                else:
                    if diff.days in settings.SUB_DAYS_NOTIFICATION:
                        try:
                            await bot.send_message(
                            user.telegram_id,
                            messages.SUB_NOTIFICATE.format(expires_at=user.expires_at.strftime("%d.%m.%Y")),
                            reply_markup=my_sub_keyboard(),    
                            parse_mode='Markdown'    
                            )
                        except:
                            pass
            elif user.status == 'expired':
                diff: timedelta = date - user.expires_at
                if diff.days == settings.EXPIRED_SUB:
                    try:
                        await bot.send_message(
                            user.telegram_id,
                            messages.OUTDATED_SUB_NOTIFICATION,
                            reply_markup=expired_user_keyboard(),
                            parse_mode='Markdown'    
                            )
                    except:
                        pass
                elif diff.days > settings.OUDATED_SUB:
                    user.status = 'outdated'
                    user.updated_at = date
                    await user_state.update_data(
                        status='outdated',
                        vpn_status='created'
                    )
                    user.vpn.status = 'created'
                    user.vpn.server_id = None
                    user.vpn.ip = None
                    user.vpn.public_key = None
                    user.vpn.updated_at = date
                    try:
                        await bot.send_message(
                            user.telegram_id,
                            messages.OUTDATED_SUB,
                            reply_markup=expired_user_keyboard(),
                            parse_mode='Markdown'    
                            )
                    except:
                        pass
            session.add(user)
            session.commit()
    await rebuild_server_config()