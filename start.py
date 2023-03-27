from aiogram.utils import executor
import asyncio
import aioschedule
from handlers.user import register_user_handlers
from handlers.admin import register_admin_handlers
from loader import dp, logger
from datetime import datetime

# регистрируем хендлеры
register_admin_handlers(dp)
register_user_handlers(dp)

# для асинхронного выполнения команд по времени
# async def scheduler():
#     aioschedule.every(30).seconds.do(check_pending_users)
#     aioschedule.every().day.at('00:02').do(rebuild_server_config)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)
   
async def on_startup(_):
    logger.info(f'Бот запущен...')
    # asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)