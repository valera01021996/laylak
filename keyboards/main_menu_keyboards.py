from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message
from test import get_locale_text
from database.tools import DBTools


def get_language_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        KeyboardButton(text="O'zbek"),
        KeyboardButton(text="Русский"),
        KeyboardButton(text="English"),
    ]
    markup.add(*buttons)
    return markup


def get_main_menu_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text=get_locale_text(lang, 'start_order'))
    )
    markup.row(
        KeyboardButton(text=get_locale_text(lang, 'settings')),
        KeyboardButton(text=get_locale_text(lang, 'leave_feedback')),
    )
    markup.row(KeyboardButton(text=get_locale_text(lang, 'cart')))
    return markup


def generate_categories_menu(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    categories = DBTools().product_tools.get_categories(lang)
    markup.add(*categories)
    markup.row(
        KeyboardButton(text=get_locale_text(lang, 'main_menu'))
    )
    return markup

def generate_products_menu(category_id, lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    products = DBTools().product_tools.get_products(category_id, lang)
    markup.add(*products)
    markup.row(
        KeyboardButton(text=get_locale_text(lang, 'main_menu')),
        KeyboardButton(text=get_locale_text(lang, 'back'))
    )
    return markup
