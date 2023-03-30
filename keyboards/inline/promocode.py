from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.buttons import button_dict

def have_promocode_keyboard(callback: types.CallbackQuery):
    """ Клавиатура с вопросом есть ли у пользователя промокод """
    markup = InlineKeyboardMarkup()

    markup.insert(InlineKeyboardButton(text='Да, есть', callback_data='yes_promocode'))

    if callback.data == 'trial_question':
        button_cb = 'activate_trial'
        text = 'Нет, активировать'
    elif callback.data == 'get_sub_question':
        button_cb = 'get_sub'
        text = 'Нет'

    markup.insert(InlineKeyboardButton(text=text, callback_data=button_cb))
    markup.row(button_dict.get('back_main'))

    return markup