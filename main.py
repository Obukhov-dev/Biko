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

    :return:
    """
    pass

# запускаем web сервер (стандартно tornado. Можно django flask fast api)
if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)


