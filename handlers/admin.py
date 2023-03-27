from aiogram import Dispatcher, types


async def admin_start(message : types.Message):
    if message.from_user.id in message.bot.get('config').tg_bot.admin_ids:
        print('Вы админ')

def register_admin_handlers(dp : Dispatcher):
    dp.register_message_handler(admin_start, commands=['admin'])