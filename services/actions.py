from db.models import Server, User
from datetime import datetime, timedelta
from loader import bot, logger, config
from db.connect import session_maker
from db.models import Order
from keyboards.inline.main import back_main_keyboard
from services.orders import check_order
from misc import messages, status
import settings

async def check_pending_orders():
    logger.info('Проверка ожидающих счетов...')
    with session_maker() as session:
        orders = session.query(Order).filter(
            Order.status == 'pending',
            ).all()
        for order in orders:
            if check_order(order):
                order.status = 'success'
                if order.user.status in ['expired','created', 'outdated']:
                    order.user.expires_at = datetime.now() + timedelta(days=order.days)
                else:
                    order.user.expires_at += timedelta(days=order.days)
                order.user.status = 'subscribed'
                order.user.updated_at = datetime.now()
                order.updated_at = datetime.now()

                try:
                    await bot.send_message(
                        chat_id=order.user.telegram_id,
                        text=messages.SUCCESS_ORDER.format(
                            id=order.id,
                            amount=order.amount,
                            status=status.ORDER_STATUS.get(order.user.status),
                            expires_at=order.user.expires_at.strftime("%d.%m.%Y")
                        ),
                        parse_mode='Markdown',
                        reply_markup=back_main_keyboard()
                    )
                except:
                    logger.warning(f'Сообщение об успешной оплате не отправлено пользователю {order.user.id}')

            else:
                diff:timedelta = datetime.now() - order.created_at
                if diff.days > settings.PENDING_ORDER_TTL:
                    order.deleted = True
                    order.status = 'expired'
                    order.updated_at = datetime.now()
                    await bot.send_message(
                        chat_id=order.user.telegram_id,
                        text=messages.DELETE_ORDER.format(
                            id=order.id,
                            amount=order.amount
                            )
                        )
            session.add(order)
            session.commit()