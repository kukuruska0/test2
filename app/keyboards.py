from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.callback_data import CallbackData


def kb_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='🛒Каталог диванов')],
        [KeyboardButton(text='👥Контакты')],
        [KeyboardButton(text='🔧Услуги')]
    ])
    return kb


def kb_main_menu_adm():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='🛒Каталог диванов')],
        [KeyboardButton(text='👥Контакты')],
        [KeyboardButton(text='🔧Услуги')],
        [KeyboardButton(text='⚙️Админ-панель')]
    ])
    return kb


def kb_adm_panel():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('✅Добавить товар'), KeyboardButton('❌Удалить товар')],
        [KeyboardButton('✉️Сделать рассылку')],
        [KeyboardButton('📢Главное меню')]
    ])
    return kb


cb = CallbackData('ikb', 'action')
cb_2 = CallbackData('ikb', 'action')


def ikb_catalog():
    ikb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton(text='Угловые', callback_data=cb.new('ug')),
         InlineKeyboardButton(text='Прямые', callback_data=cb.new('pr'))],
        [InlineKeyboardButton(text='Еврокнижка', callback_data=cb.new('evro')),
         InlineKeyboardButton(text='Пантограф', callback_data=cb.new('pan'))],
        [InlineKeyboardButton(text='Аккордион', callback_data=cb.new('akk'))]
    ])
    return ikb


def ikb_catalog_delete():
    ikb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton(text='Угловые', callback_data=cb_2.new('ug1')),
         InlineKeyboardButton(text='Прямые', callback_data=cb_2.new('pr1'))],
        [InlineKeyboardButton(text='Еврокнижка', callback_data=cb_2.new('evro1')),
         InlineKeyboardButton(text='Пантограф', callback_data=cb_2.new('pan1'))],
        [InlineKeyboardButton(text='Аккордион', callback_data=cb_2.new('akk1'))]
    ])
    return ikb


def cancel():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('❌Отмена'))
    return kb


def ikb_malling_check():

    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Рассылка без фото', callback_data=cb.new('text'))],
        [InlineKeyboardButton(text='Рассылка с фото', callback_data=cb.new('photo'))]
    ])
    return ikb



