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

        self.next_step_handlers = {
            "teleid": [lambda: print(end=''), {}]
        }

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

wsc = wsclient.WsClient(b, "ws://10.82.91.102:3333")

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
        "Получение дрона", callback_data=f"drone.{msg.from_user.id}"
    ))
    b.roles[str(msg.from_user.id)]["last_msg"] = (await b.send_message(msg.chat.id, "оаоаоа", reply_markup=mk)).id

@b.callback_query_handler(lambda call: call.data.split('.')[0]=="drone")
async def call_drone(call: tb.CallbackQuery):
    #if not await b.check_access(call.message, 1): return
    args = call.data.split('.')
    await b.edit_message_text("Введи uid c дрона", call.message.chat.id, b.roles[str(call.message.chat.id)]["last_msg"])
    b.next_step_handlers[args[1]] = [request_drone, {}]

async def request_drone(msg: tb.Message, data: dict):
    print("але туда")
    wsc.send_with_order({"op": "drone", "data": {"drone_uid": msg.text}}, msg.from_user.id)
    b.next_step_handlers[str(msg.from_user.id)] = False

PROBE_TYPES_INFO = {
    "rain": "Осадки",
    "lake": "Водоем"
}

async def resp_for_drone(resp: dict, user_id: str):
    print("Але сюда")
    if resp["code"] == "25":
        await b.send_message(user_id, "Дрон с таким uid не найден")
        return
    if resp["code"] == "26":
        await b.send_message(user_id, f"Проба уже взята. Ее uid: {resp['info']['probe_uid']} . Тип: {PROBE_TYPES_INFO[resp['info']['probe_type']]}")
        return
    if not resp["code"] == "10":
        await b.send_message(user_id, "Произошла неизвестная ошибка")
        ##представьте отправку разработчику
        return
    await b.send_message(user_id, f"Информация о пробе получена. Ее uid: {resp['info']['probe_uid']} . Тип: {PROBE_TYPES_INFO[resp['info']['probe_type']]}")
wsc.end_points["drone"] = resp_for_drone

@b.message_handler(commands=["super_data"])
async def super_data(msg: tb.Message):
    if not await b.check_access(msg, 7): return
    try: data = json.loads(" ".join(msg.text.split()[1:]))
    except Exception:
        await b.send_message(msg.chat.id, "Ошибка при конвертировании аргумента")
        return
    wsc.send_with_order({"op": "super_data", "data": data}, msg.from_user.id)
    await b.send_message(msg.chat.id, "Запрос отправлен")

async def resp_for_super_data(resp: dict, user_id: str):
    if resp["code"] == "24":
        await b.send_message(user_id, "Не достаточно полей")
        return
    if resp["code"] == "27":
        await b.send_message(user_id, "Коллекиция не найдена")
        return
    if resp["code"] == "28":
        await b.send_message(user_id, "По фильтру не получилось значений или больше одного значения, replace не удался")
        return
    if not resp["code"] == "10":
        await b.send_message(user_id, "Произошла не предвиденная ошибка")
        #ага
        return
    await b.send_message(user_id, json.dumps(resp["info"]["values"], indent=4))
wsc.end_points["super_data"] = resp_for_super_data

@b.message_handler(content_types=["text"])
async def text_type(msg: tb.Message):
    if str(msg.from_user.id) in b.next_step_handlers.keys():
        if b.next_step_handlers[str(msg.from_user.id)]:
            await b.next_step_handlers[str(msg.from_user.id)][0](msg, b.next_step_handlers[str(msg.from_user.id)][1])
            return
    await b.send_message(msg.chat.id, "оаоао")

thrd.Thread(target=wsc.run).start()

b._run()