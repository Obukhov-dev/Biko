from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js

# Для ..
import asyncio

#
chat_msgs = []
online_users = set()

# Максимальное количесвто сообщений
MAX_MESSAGES_COUNT = 100


async def main():
    """
    Главная функция при открытии приложения.

    :return:
    """
    #Все glob сообщения
    global chat_msgs

    put_markdown("## Привет! Это web мессенджер Biko. \n Укажите свой ник и общайтесь свободно.")
    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nickname = await input("Войти в чат", required=True, placeholder="Ваш ник Под ним вас будут видеть другие пользователи 🤫 🤩 😄",validate=lambda n: 'Такой ник уже используется' if n in online_users or n == '!!!' else None)
    online_users.append(('!!!!', f"{nickname} - присоединился к чату"))

    pass

# запускаем web сервер (стандартно tornado. Можно django flask fast api)
if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)


