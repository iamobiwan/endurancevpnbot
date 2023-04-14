from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy import and_
from db.connect import session_maker
from db.models import User, Order, Plan
import settings
from datetime import datetime
from loader import logger, config
import requests


def get_user_orders(user_id):
    with session_maker() as session:
        orders = session.query(Order).filter(and_(
            Order.user_id == user_id,
            Order.deleted == False
        )
            ).all()
        return orders

def get_order(order_id):
    with session_maker() as session:
        order = session.query(Order).where(
            Order.id == order_id
            ).first()
        return order

def delete_order(order_id):
    with session_maker() as session:
        order = session.query(Order).where(
            Order.id == order_id
            ).first()
        order.deleted = True
        order.status = 'deleted'
        order.updated_at = datetime.now()
        session.add(order)
        session.commit()

async def create_order(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    with session_maker() as session:
        user_data = await state.get_data()
        user = session.query(User).filter(User.telegram_id == callback.from_user.id).first()
        orders = session.query(Order).filter(and_(
            Order.user_id == user_data.get('id'),
            Order.deleted == False,
            Order.status != 'success'
        )).all()
        
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
    
def check_order(order):
    url = f'https://yoomoney.ru/api/operation-history'
    headers = {
        'Authorization': f'Bearer {config.donate.y_token}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = {
        'label': order.label,
        # 'type': 'deposition',
        # 'records': 3,
        # 'details': 'true'
        # 'operation_id': '714571374770005004'
    }
    response = requests.post(url, headers=headers, data=params)
    try:
        operations = response.json().get('operations')
    except:
        operations = None
    if operations:
        if operations[0].get('status') == 'success':
            logger.info(f'Счет {order.id} оплачен.')
            return True
    else:
        return False