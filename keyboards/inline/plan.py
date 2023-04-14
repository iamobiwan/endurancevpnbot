from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.dispatcher import FSMContext
from db.models import User, Plan
from keyboards.buttons import button_dict
from services.plans import get_user_and_plans
from keyboards.callback import plan_callback, order_callback

def plans_keyboard(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    user, plans = get_user_and_plans(callback.from_user.id)
    for plan in plans:

        if user.discount:
            button_text = f'{plan.days} дней за {plan.amount - user.discount}₽ (было {plan.amount}₽)'
        else:
            button_text = f'{plan.days} дней за {plan.amount}₽'

        markup.row(
            InlineKeyboardButton(
                text=button_text,
                callback_data=plan_callback.new(location=callback.data, plan_id=plan.id)
            )
        )

    if callback.data == 'get_sub':
        markup.row(button_dict.get('back_main'))
    elif callback.data == 'extend_sub':
        markup.row(button_dict.get('back_my_sub'))

    return markup