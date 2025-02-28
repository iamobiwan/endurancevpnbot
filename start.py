from aiogram.utils import executor
import asyncio
import aioschedule
from handlers.admin import register_admin_handlers
from handlers.main import register_main_handlers
from handlers.subscribe import register_sub_handlers
from handlers.promocode import register_promocode_handlers
from handlers.plan import register_plan_handlers
from handlers.orders import register_orders_handlers
from handlers.vpn import register_vpn_handlers
from handlers.instruction import register_instruction_handlers
from handlers.support import register_support_handlers
from services.actions import check_pending_orders, check_pending_vpn, rebuild_server_config, check_sub_expire
from loader import dp, logger
from datetime import datetime

# регистрируем хендлеры
# register_admin_handlers(dp)
register_main_handlers(dp)
# register_sub_handlers(dp)
# register_plan_handlers(dp)
# register_promocode_handlers(dp)
# register_orders_handlers(dp)
# register_vpn_handlers(dp)
# register_instruction_handlers(dp)
# register_support_handlers(dp)

# для асинхронного выполнения команд по времени
# async def scheduler():
    # aioschedule.every(30).seconds.do(check_pending_orders)
    # aioschedule.every(60).seconds.do(check_pending_vpn)
    # aioschedule.every(90).seconds.do(check_sub_expire)
    # aioschedule.every(120).seconds.do(rebuild_server_config)
    # aioschedule.every(5).minutes.do(check_pending_vpn)
    # aioschedule.every(7).minutes.do(check_pending_orders)
    # aioschedule.every().day.at('01:00').do(check_sub_expire)
    # while True:
    #     await aioschedule.run_pending()
    #     await asyncio.sleep(1)
   
async def on_startup(_):
    logger.info(f'Бот запущен...')
    # asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)