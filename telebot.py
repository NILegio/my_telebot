from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
import db_bot

TOKEN = "" #для своего токена
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await msg.reply('Я бот.Приятно познакомиться,{0}.\n'
                    'Чтобы узнать наименование товара, используйте команду /get_brand <артикул товара> \n'
                    'Чтобы узнать бренд товара, используйте команду /get_title <артикул товара>'.format(msg.from_user.first_name))

@dp.message_handler(commands='get_brand')
async def get_brand(msg: types.Message):
    vendor_code = msg.get_args()
    brand = await get_data("brand_name", vendor_code)
    db_bot.create_goods(vendor_code, brand, "brand")
    await msg.answer(brand)

@dp.message_handler(commands='get_title')
async def get_brand(msg: types.Message):
    vendor_code =  msg.get_args()
    title = await get_data("imt_name",vendor_code)
    db_bot.create_goods(vendor_code, title, "title")
    await msg.answer(title)

async def get_data(key, request_id):
    url = "https://wbx-content-v2.wbstatic.net/ru/{0}.json"
    wild_json = requests.get(url.format(request_id))
    if wild_json.status_code != 200:
        return "Неверно указан артикул товара"
    path = find_with_key(key, wild_json.json())

    return retrieve(wild_json.json(), next(path))

def find_with_key(wanted_key, tree, path=tuple()):
    if isinstance(tree, list):
        for i, elem in enumerate(tree):
            yield from find_with_key(wanted_key, elem, path+(i,))

    if isinstance(tree, dict):
        for key, value in tree.items():
            if key == wanted_key: yield path+(key,)
            yield from find_with_key(wanted_key, value, path+(key,))

def retrieve(tree, path):
    for p in path:
        tree = tree[p]
    return tree


if __name__ == '__main__':
    db_bot.create_db()
    executor.start_polling(dp)