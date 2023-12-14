import os

import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from app import *

load_dotenv()
storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db_start()
    print('Bot started!!!')


class NewOrder(StatesGroup):
    type = State()
    photo = State()
    name = State()
    desc = State()
    price = State()


class MallingState(StatesGroup):
    Choice = State()
    Input = State()
    Input_text = State()
    Input_photo = State()
    Input_photo_2 = State()


def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5, key_prefix='antiflood_'):
        BaseMiddleware.__init__(self)
        self.rate_limit = limit
        self.prefix = key_prefix

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dsp = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_key_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f'{self.prefix}_{handler.__name__}')
        else:
            limit = self.rate_limit
            key = f'{self.prefix}_message'
        try:
            await dsp.throttle(key, rate=limit)

        except Throttled as _t:
            await self.msg_throttle(message, _t)
            raise CancelHandler

    async def msg_throttle(self, message: types.Message, throttle: Throttled):
        delta = throttle.rate - throttle.delta
        if throttle.exceeded_count <= 2:
            await message.answer('Подождите 5 секунд')
        await asyncio.sleep(delta)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await cmd_start_db(message.from_user.id)
    await bot.send_photo(chat_id=message.from_user.id,
                         caption=f'{message.from_user.first_name}, Добро пожаловать в наш магазин!👋\n'
                                 f'Фабрика <b>StilKom</b> с 2008 года занимается изготовлением и ремонтом мягкой '
                                 f'мебели различного'
                                 f' назначения. Наша команда опытных мастеров воплотит смелые дизайнерские идеи с '
                                 f'учетом всех'
                                 f' пожеланий заказчика и подарит изделиям вторую жизнь в минимальные сроки.',
                         reply_markup=kb_main_menu(), parse_mode='html',
                         photo='AgACAgIAAxkBAAMCZT7BsVrxSDJNYRaYD7dknIMjKdAAAqrQMRvcM_hJpTcSywcp2csBAAMCAAN5AAMwBA')
    if message.from_user.id == int(os.getenv('ADMIN')):
        await message.answer('Вы авторизовались как администратор🔧', reply_markup=kb_main_menu_adm())


@dp.message_handler(Text(equals='📢Главное меню'), state=MallingState.Input)
async def main_menu_cmd_2(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Вы в главном меню📢', reply_markup=kb_main_menu_adm())


@dp.message_handler(Text(equals='📢Главное меню'), state=NewOrder.type)
async def main_menu_cmd_2(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Вы в главном меню📢', reply_markup=kb_main_menu_adm())


@dp.message_handler(Text(equals='📢Главное меню'))
async def main_menu_cmd(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN')):
        await message.answer('Вы в главном меню📢', reply_markup=kb_main_menu_adm())

    else:
        await message.answer('Вы в главном меню📢', reply_markup=kb_main_menu())


@dp.message_handler(Text(equals='👥Контакты'))
async def contact_cmd(message: types.Message):
    await message.answer(text='<b>🏢 Адреса</b>:\nс. Петровское, ул. Заводская, д. 1А\n'
                              'г. Москва Боровское ш., д. 51 (м. Новопеределкино)\n'
                              'г. Москва Рязанский проспект, 86/1 ст3\n\n<b>📞 Номера телефона</b>:\n'
                              '+7 (925) 087-47-08\n+7 (495) 135-92-55\n\n<b>📫 Почта</b>:\n'
                              'info@stilkom.ru\n\n<b>⏰ График работы</b>:\nПн-Пт 09:00-18:00\n'
                              'Сб, Вс — выходной', parse_mode='html')


@dp.message_handler(Text(equals='🔧Услуги'))
async def job_cmd(message: types.Message):
    await message.answer(
        '📌 Изготовление мебели по вашему дизайну(Кровати, диваны, кресла, стулья и др.)\n\n'
        '📌 Ремонт, перетяжка, реставрация мебели(Кровати, диваны, кресла, стулья и др.)\n\n'
        '📌 Ремонт кухонной мебели\n\n'
        '📌 Изготовление стеновых панелей\n\n'
        '📌 Ремонт кожаной мебели\n\n'
        '📌 Ремонт медицинской мебели\n\n'
        '📌 Ремонт офисной мебели\n\n'
        '📌 Мебель оптом\n\n'
        '<b>Оформить заявку</b>:\n'
        'https://stilkom.ru/uslugi/', parse_mode='html')


@dp.message_handler(Text(equals='⚙️Админ-панель'))
async def admin_cmd(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN')):
        await message.answer('Вы в админ панели⚙️', reply_markup=kb_adm_panel())
    else:
        pass


@dp.message_handler(Text(equals='✉️Сделать рассылку'))
async def malling_create(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN')):
        await MallingState.Choice.set()
        await message.answer('Выбирете вид рассылки', reply_markup=ikb_malling_check())
        await MallingState.Input.set()


@dp.callback_query_handler(cb_2.filter(action='text'), state=MallingState.Input)
async def text_malling(callback: types.CallbackQuery):
    await callback.answer('Вид выбран')
    await callback.message.answer('Введите текст рассылки', reply_markup=cancel())
    await MallingState.Input_text.set()


@dp.message_handler(state=MallingState.Input_text)
async def malling_cmd_text(message: types.Message, state: FSMContext):
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    users = cur.execute("SELECT tg_id FROM accounts").fetchall()
    db.close()
    for user in users:
        await bot.send_message(chat_id=user[0], text=message.text)
    await message.answer('Расссылка прошла успешно✅', reply_markup=kb_adm_panel())
    await state.finish()


@dp.callback_query_handler(cb_2.filter(action='photo'), state=MallingState.Input)
async def photo_malling(callback: types.CallbackQuery):
    await callback.answer('Вид выбран')
    await callback.message.answer('Введите текст рассылки',
                                  reply_markup=cancel())
    await MallingState.Input_photo.set()


@dp.message_handler(state=MallingState.Input_photo)
async def save_caption(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(text=answer)
    await message.answer('Пришлите фото для рассылки', reply_markup=cancel())
    await MallingState.Input_photo_2.set()


@dp.message_handler(lambda message: not message.photo, state=MallingState.Input_photo_2)
async def check_photo(message: types.Message):
    await message.answer('Это не фотография❌!!!')


@dp.message_handler(state=MallingState.Input_photo_2, content_types=['photo'])
async def save_photo(message: types.Message, state: FSMContext):
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    users = cur.execute("SELECT tg_id FROM accounts").fetchall()
    db.close()
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    for user in users:
        await bot.send_photo(chat_id=user[0], photo=photo, caption=text)
    await message.answer('Рассылка прошла успешно✅', reply_markup=kb_adm_panel())
    await state.finish()


@dp.message_handler(Text(equals='❌Отмена'), state='*')
async def cancel_cmd(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие завершено❌', reply_markup=kb_adm_panel())


@dp.message_handler(Text(equals='✅Добавить товар'))
async def add_order(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN')):
        await NewOrder.type.set()
        await message.answer('1)Выберите тип товара', reply_markup=ikb_catalog())
    else:
        pass


@dp.callback_query_handler(state=NewOrder.type)
async def add_type(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = callback.data
    await callback.answer('Тип товара выбран')
    await callback.message.answer('2)Пришлите фото товара', reply_markup=cancel())
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def check_photo(message: types.Message):
    await message.answer('Это не фотография❌!!!')


@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.answer('3)Пришлите наименование товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.name)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('4)Пришлите описание товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def add_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('5)Пришлите цену товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await add_item(state)
    await message.answer('Товар успешно создан✅', reply_markup=kb_adm_panel())
    await state.finish()


@dp.message_handler(Text(equals='❌Удалить товар'))
async def delete_cmd(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN')):
        await message.answer('Выбирете категорию товара', reply_markup=ikb_catalog_delete())


@dp.callback_query_handler(cb_2.filter(action='ug1'))
async def delete2_cmd(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:ug'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
        ikb = InlineKeyboardMarkup(row_width=2)
        ikb.add(InlineKeyboardButton(text=f'Удалить {ret[1]}', callback_data=f'del {ret[1]}'))
        await bot.send_message(chat_id=callback.from_user.id, text='^^^^^^', reply_markup=ikb)


@dp.callback_query_handler(cb_2.filter(action='pr1'))
async def delete2_cmd(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:pr'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
        ikb = InlineKeyboardMarkup(row_width=2)
        ikb.add(InlineKeyboardButton(text=f'Удалить {ret[1]}', callback_data=f'del {ret[1]}'))
        await bot.send_message(chat_id=callback.from_user.id, text='^^^^^^', reply_markup=ikb)


@dp.callback_query_handler(cb_2.filter(action='evro1'))
async def delete2_cmd(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:evro'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
        ikb = InlineKeyboardMarkup(row_width=2)
        ikb.add(InlineKeyboardButton(text=f'Удалить {ret[1]}', callback_data=f'del {ret[1]}'))
        await bot.send_message(chat_id=callback.from_user.id, text='^^^^^^', reply_markup=ikb)


@dp.callback_query_handler(cb_2.filter(action='pan1'))
async def delete2_cmd(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:pan'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
        ikb = InlineKeyboardMarkup(row_width=2)
        ikb.add(InlineKeyboardButton(text=f'Удалить {ret[1]}', callback_data=f'del {ret[1]}'))
        await bot.send_message(chat_id=callback.from_user.id, text='^^^^^^', reply_markup=ikb)


@dp.callback_query_handler(cb_2.filter(action='akk1'))
async def delete2_cmd(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:akk'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
        ikb = InlineKeyboardMarkup(row_width=2)
        ikb.add(InlineKeyboardButton(text=f'Удалить {ret[1]}', callback_data=f'del {ret[1]}'))
        await bot.send_message(chat_id=callback.from_user.id, text='^^^^^^', reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def delete3_cmd(callback: types.CallbackQuery):
    await db_delete(callback.data.replace('del ', ''))
    await callback.answer(text=f'{callback.data.replace("del ", "")} удалена', show_alert=True)


@dp.message_handler(Text(equals='🛒Каталог диванов'))
async def catalog_cmd(message: types.Message):
    await message.answer('Выбирете категорию товара', reply_markup=ikb_catalog())


@dp.callback_query_handler(cb.filter(action='ug'))
async def catalog_sofa(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:ug'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
    db.close()


@dp.callback_query_handler(cb.filter(action='pr'))
async def catalog_sofa(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:pr'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
    db.close()


@dp.callback_query_handler(cb.filter(action='evro'))
async def catalog_sofa(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:evro'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
    db.close()


@dp.callback_query_handler(cb.filter(action='pan'))
async def catalog_sofa(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:pan'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
    db.close()


@dp.callback_query_handler(cb.filter(action='akk'))
async def catalog_sofa(callback: types.CallbackQuery):
    await callback.answer('Категория выбрана')
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    for ret in cur.execute("SELECT * FROM items WHERE type == 'ikb:akk'").fetchall():
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=ret[0],
                             caption=f'{ret[1]}\n<b>Описание</b>:\n{ret[2]}\n<b>Цена:</b>\n<em>{ret[3]}</em>\n'
                                     f'<b>Заказать можно тут</b>: '
                                     f'https://stilkom.ru/myagkaya-mebel-ot-proizvoditelya/divan-ot-proizvoditelya/',
                             parse_mode='html')
    db.close()


if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True)
