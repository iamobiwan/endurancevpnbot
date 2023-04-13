WELCOME = """Привет!

Этот бот предоставит Вам быстрый и безопасный доступ к сети Интернет \
при помощи VPN.

Перейди в *Главное меню* чтобы управлять ботом.
"""

MAIN_MENU_CREATED = """Добро пожаловать, *{name}*!

Список команд доступен в меню бота внизу слева.

Не забудь активировать *ПРОМОКОД*, если он у тебя есть, а потом поделиться \
с друзьями своим промокодом, чтобы получить скидку *100₽* за каждого приведенного друга!

VPN работает по подписке. Для использования VPN оформите подписку \
или активируйте пробный период на 3 дня.
"""

MAIN_MENU = """Добро пожаловать в *Главное меню*!

Здесь ты можешь управлять своей подпиской, получить настройки для VPN \
или инструкцию по установке.

Выбери команду из списка ниже:                                
"""

MAIN_MENU_EXPIRED = """Добро пожаловать в *Главное меню*!

К сожалению, твоя подписка закончилась \U0001f614 

Чтобы продолжить пользоваться VPN продли подписку.
"""

BLOCK_TRIAL = "Вы не можете активировать пробный период!"

SUCCESS_TRIAL = """Благодарю за активацию пробного периода!

Пробный период заканчивается {date},
"""

MY_SUB = """ \U00002b50 *Моя подписка*

Статус вашей подписки: *{status}*
Дата окончания: *{date}*

Выберите команду из списка ниже или нажмите "Menu" для того, чтобы увидеть весь список команд
"""

HAVE_PROMOCODE = """Не забудьте активировать промокод, если он у вас есть!

Найти его можно в меню "Моя подписка" \U000027a1 "Мой промокод"
"""

ALREADY_USE_PROMOCODE = """Вы уже использовали промокод!

Теперь поделитесь своим с друзьями!
"""

ENTER_PROMOCODE = """Введите промокод:"""

NO_PROMOCODE = """Такого промокода не существует!
"""

SUCCESS_PROMOCODE = """Промокод применен!

Ваша скидка будет применена при следующем продлении подписки.
"""

APPLY_PROMOCODE = """ Ваш промокод:

`{code}`

Поделитесь им с друзьями, чтобы получить скидку *100₽* на следующее продление за каждого приведенного друга!

Максимальная скидка составляет
"""

DETAIL_ORDER = """Ваш заказ *№{id}*.

Сумма: *{amount}₽*
Количество дней: *{days}*
Статус: *{status}*
"""

MAX_ORDERS = """У вас максимальное количество заказов!
Удалите или оплатите имеющиеся заказы.
"""

ORDERS = """*Ваши заказы*

Неоплаченные заказы автоматически удаляются через 24 часа
"""

NO_ORDERS = """У вас нет созданных или не оплаченых заказов.
"""

SUCCESS_ORDER = """Ваш счет *№{id}* на сумму *{amount}₽* оплачен.

Статус вашей подписки: *{status}*
Дата окончания: *{expires_at}*
"""

DELETE_ORDER ="""Ваш счет {id} на сумму {amount}₽ удален.\n\n'"""

NOTIFY_DELETE_ORDER ="""Ваш счет {id} на сумму {amount}₽ в статусе {status} скоро будет удален."""

DISCOUNT_FOR_INVITING_USER = """По вашему промокоду была активирована подписка!

Теперь Ваша скидка увеличилась на *100₽*
"""

MAX_DISCOUNT_FOR_USER = """По вашему промокоду была активирована подписка!

У вас уже максимальная скидка, поэтому вам не было начислено бонусов.

Продлите подписку с текущей скидкой, чтобы обнулить количество бонусов.
"""

GET_VPN_UNSUB = """У вас отсутствует *подписка*.

Чтобы получить настройки, оформите или продлите подписку.
"""

REQUEST_FOR_VPN = """Мы получили Ваш запрос на формирование настроек.

В течение 5 минут бот обработает Ваш запрос и пришлет настройки.

Ожидайте...
"""

WAIT_FOR_SETTINGS = """Ваши настройки формируются.

В течение 5 минут бот обработает Ваш запрос и пришлет настройки

Ожидайте...
"""

GET_SETTINGS_SUCCESS = """Вот ваш файл настроек \U0000261d

Чтобы воспользоваться им, прочитайте инструкцию в
"Главном меню" или запросите их у бота командой /instruction
"""

GET_SETTING_ERROR = """К сожалению, что-то пошло не так, обратитесь \
в техническую поддержку: @endurancevpnsupport
"""

EXPIRED_SUB = """Срок действия Вашей подписки истек. \U00002639

Чтобы продолжить пользоваться VPN продлите подписку.
"""

SUB_NOTIFICATE = """Срок действия Вашей подписки скоро закончится.

Дата окончания: *{expires_at}*
Чтобы продолжить пользоваться VPN продлите подписку.
"""

OUTDATED_SUB_NOTIFICATION = """Срок действия Вашей подписки давно истек.

Если вы не продлите подписку в течении *7* дней, ваши настройки VPN будут удалены.
"""

OUTDATED_SUB = """Срок действия Вашей подписки давно истек.

Ваши настройки VPN будут удалены. Для формирования новых настроек продлите подписку.
"""