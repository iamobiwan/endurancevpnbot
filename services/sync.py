from paramiko import SSHClient, AutoAddPolicy
import os
from loader import bot, logger, config
from misc import messages
from db.models import Server


@logger.catch
async def sync_config(server: Server):
    logger.info(f'Начинаю синхронизацию конфигурации сервера {server.name}...')
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.load_system_host_keys()
    try:
        client.connect(server.wan_ip, username='root', timeout=5)
        sftp = client.open_sftp()
        sftp.put(f'servers/{server.name}/wg0.conf', '/etc/wireguard/wg0.conf')
        logger.info('Файл скопирован')
        if sftp.stat('/etc/wireguard/wg0.conf').st_size == os.stat(f'servers/{server.name}/wg0.conf').st_size:
            logger.info('Успешно синхронизировано')
        else:
            logger.warning('Не синхронизировано') 
    except TimeoutError:
        for admin_id in bot.get('config').tg_bot.admin_ids:
            await bot.send_message(
                chat_id=admin_id,
                text=messages.ADMIN_SYNC_TIMEOUT_ERROR.format(server=server.name),
                parse_mode='Markdown'
            )
            logger.warning(f'Не удается подключиться к серверу {server.name}, синхронизация не выполнена')
    except:
        for admin_id in bot.get('config').tg_bot.admin_ids:
            await bot.send_message(
                chat_id=admin_id,
                text=messages.ADMIN_SYNC_ERROR.format(server=server.name),
                parse_mode='Markdown'
            )
            logger.warning(f'Синхронизация сервера {server.name}не выполнена')


@logger.catch
async def check_config(server: Server):
    logger.info('Начинаю проверку конфигурации...')
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.load_system_host_keys()
    try:
        client.connect(server.wan_ip, username='root', timeout=5)
        sftp = client.open_sftp()
        remote_file = sftp.open('/etc/wireguard/wg0.conf').read()
        with open(f'servers/{server.name}/wg0.conf', 'rb') as f:
            local_file = f.read()
            if local_file == remote_file:
                logger.info('Файлы идентичны')
            else:
                logger.warning('Файлы не совпадают!')
                for admin in config.tg_bot.admin_ids:
                    await bot.send_message(admin, f'Конфигурация не залилась на сервер {server.name}, ip: {server.wan_ip}')
                    logger.warning(f'Конфигурация сервера {server.name}, ip: {server.wan_ip} не обновилась!')
    except TimeoutError:
        for admin_id in bot.get('config').tg_bot.admin_ids:
            await bot.send_message(
                chat_id=admin_id,
                text=messages.ADMIN_CHECK_TIMEOUT_ERROR.format(server=server.name),
                parse_mode='Markdown'
            )
            logger.warning(f'Не удается подключиться к серверу {server.name}, проверка не выполнена')
    except:
        for admin_id in bot.get('config').tg_bot.admin_ids:
            await bot.send_message(
                chat_id=admin_id,
                text=messages.ADMIN_CHECK_ERROR.format(server=server.name),
                parse_mode='Markdown'
            )
            logger.warning(f'Проверка сервера {server.name} не выполнена')

