from aiogram.types import InlineKeyboardButton

button_dict = {}
buttons: tuple = (
    ('\U000026a1 Главное меню', 'main'),
    ('\U0000231B Активировать пробный период', 'activate_trial'),
    ('\U00002b50 Моя подписка', 'my_sub'),
    ('\U00002b50 Оформить подписку', 'get_sub'),
    ('\U00002b50 Продлить подписку', 'extend_sub'),
    ('\U0001f91d Применить промокод', 'get_discount'),
    ('\U0001f527 Получить настройки', 'get_settings'),
    ('\U0001f91d Мой промокод', 'get_promocode'),
    ('\U0001f4cb Мои заказы', 'orders'),
    ('\U0001f4d2 Инструкция', 'get_instruction'),
    ('\U000025c0 Назад', 'back_main'),
    ('\U000025c0 Назад', 'back_my_sub'),
)

for text, callback in buttons:
    button_dict.update({callback: InlineKeyboardButton(text=text, callback_data=callback)})