from telebot.async_telebot import AsyncTeleBot
import telebot.types as tb

import wsclient

import asyncio

import json
import threading as thrd

class SiburOpenEcoMap(AsyncTeleBot):
    def __init__(self):
        super().__init__(json.load(open("cfg.json"))["token"], parse_mode="markdown")
        self.roles = json.load(open("roles.json"))
        self.loop = None

    def update_db_roles(self): json.dump(self.roles, open("roles.json", 'w'))

    def _run(self):
        asyncio.run(self._async_run())

    async def _async_run(self):
        self.loop = asyncio.get_running_loop()
        await self.polling(True)

    async def check_access(self, msg: tb.Message, access_level: float):
        if not str(msg.from_user.id) in self.roles.keys():
            await b.send_message(msg.chat.id, "Доступ запрещен")
            return False
        if not self.roles[str(msg.from_user.id)]["role"] >= access_level:
            await b.send_message(msg.chat.id, "Доступ запрещен")
            return False
        return True

b = SiburOpenEcoMap()

wsc = wsclient.WsClient(b)

@b.message_handler(commands=["rolechange"])
async def c_rolechange(msg: tb.Message):
    if not await b.check_access(msg, 10): return
    args = msg.text.split()
    if not len(args) >= 3:
        await b.send_message(msg.chat.id, "rolechange id role")
        return
    try: float(args[2])
    except Exception:
        await b.send_message(msg.chat.id, "Второй аргумент не float")
        return
    b.roles[args[1]] = {"role": float(args[2])}
    b.update_db_roles()
    await b.send_message(msg.chat.id, f"Для {args[1]} установлена роль {args[2]}")

@b.message_handler(commands=["rolelist"])
async def c_rolelist(msg: tb.Message):
    if not await b.check_access(msg, 10): return
    await b.send_message(msg.chat.id, json.dumps(b.roles, indent=4))

@b.message_handler(commands=["roleremove"])
async def c_roleremove(msg: tb.Message):
    if not await b.check_access(msg, 10): return
    args = msg.text.split()
    if not len(args) >= 2:
        await b.send_message(msg.chat.id, "roleremove id")
        return
    if not args[1] in b.roles.keys():
        await b.send_message(msg.chat.id, f"Пользователь для удаления {args[1]} не найден")
        return
    del b.roles[args[1]]
    b.update_db_roles()
    await b.send_message(msg.chat.id, f"Пользователь {args[1]} удален")

@b.message_handler(commands=["start", "main"])
async def c_start_main(msg: tb.Message):
    if not await b.check_access(msg, 1): return
    mk = tb.InlineKeyboardMarkup()
    mk.add(tb.InlineKeyboardButton(
        "Получение дрона", f"drone.{msg.from_user.id}"
    ))
    b.roles[str(msg.from_user.id)]["last_msg"] = await b.send_message(msg.chat.id, "оаоаоа", reply_markup=mk).id

thrd.Thread(target=wsc.run).start()

b._run()