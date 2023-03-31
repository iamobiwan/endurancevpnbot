from aiogram import types
from aiogram.dispatcher import FSMContext
from db.connect import session_maker
from db.models import User, Order, Plan
import settings
from datetime import datetime
from loader import logger, config


def get_user_orders(user_id):
    with session_maker() as session:
        orders = session.query(Order).filter(
            Order.user_id == user_id,
            ).all()
        return orders

async def create_order(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    with session_maker() as session:
        user_data = await state.get_data()
        user = session.query(User).filter(User.telegram_id == callback.from_user.id).first()
        orders = session.query(Order).filter(
            Order.user_id == user_data.get('id'),
            ).all()
        
        if len(orders) >= settings.MAX_ORDERS_CNT:
            return False
        else:
            plan = session.query(Plan).filter(Plan.id == callback_data.get('plan_id')).first()
            label = f'{user.id}-{datetime.now().strftime("%d%m%Y%H%M%S")}'
            amount = plan.amount - user.discount
            order = Order(
                user_id=user_data.get('id'),
                status='pending',
                amount = amount,
                label=label,
                days=plan.days,
                donate_url = settings.DONATE_URL.format(
                    wallet=config.donate.y_wallet,
                    amount=amount,
                    label=label
                ),
                invite_discount=user_data.get('invite_discount'),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            if user.discount:
                user.discount = 0
                user.updated_at = datetime.now()
                session.add(user)

            if user_data.get('invite_discount'):
                await state.update_data(
                    invite_discount=False
                )

            session.add(order)
            session.commit()
            logger.info(f'Создан счет id={order.id} для пользователя {user.name} id={user.id}')
            return order