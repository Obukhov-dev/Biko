from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js

# Для ..
import asyncio

#
chat_msgs = []
online_users = set()

# Максимальное количество сообщений в чате
MAX_MESSAGES_COUNT = 100


async def main():
    """
    Главная функция при открытии приложения.

    :return:
    """
    # Все glob сообщения
    global chat_msgs

    put_markdown("## Biko \n Защищенный. Быстрый. Свободный.")
    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)
    nickname = await input("Войти в чат", required=True, placeholder="Ваше имя",
                           validate=lambda n: "Такой ник уже используется!" if n in online_users or n == '📢' else None)
    online_users.add(nickname)

    chat_msgs.append(('🔊 ', f'`{nickname}` присоединился к чату!'))
    msg_box.append(put_markdown(f'🔊 `{nickname}` присоединился к чату'))

    # функция асинхронного обновление списка сообщений
    refresh_task = run_async(refresh_msg(nickname, msg_box))

    # Бесконечный цикл в ожидании отправки сообщения юзверем
    while True:
        data = await input_group("💬 Новое сообщение", [
            input(placeholder="Текст сообщения", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label': 'Выйти из чата', 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"`{nickname}` : {data['msg']}"))
        chat_msgs.append((nickname, data['msg']))

    # exit chat
    refresh_task.close()

    online_users.remove(nickname)
    toast("Вы вышли из чата")
    msg_box.append(put_markdown(f"🔊  `{nickname}` покинул чат"))
    chat_msgs.append(('🔊', f"  `{nickname}` покинул чат"))

    put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))


# Сама функция для обновления списка сообщений в чате, которая каждую 1 секунду обновляет чат.
async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        # каждую 1 - секунду
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:
                msg_box.append(put_markdown(f"`{m[0]}` : {m[1]}"))

        # Очищаем все сообщения, которые больше предела Max_messages_count
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)


# запускаем web сервер (стандартно tornado. Можно django flask fast api)
if __name__ == "__main__":
    start_server(main, debug=True, port=5000, cdn=False)
