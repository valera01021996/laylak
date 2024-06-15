from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from database.tools import DBTools
from test import get_locale_text


def generate_cart_menu(cart_id: int, lang):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text=get_locale_text(lang, "checkout"), callback_data=f"create-order_{cart_id}")
    )
    return markup


def generate_cart_menu_reply_markup(chat_id, lang):
    markup = ReplyKeyboardMarkup(row_width=2)
    user_id = DBTools().user_tools.get_user_id(chat_id)
    product_names = DBTools().cart_tools.get_cart_product(user_id)

    for name in product_names:
        name = str(*name)
        markup.add(
            KeyboardButton(text='❌    ' + name)
        )

    markup.row(
        KeyboardButton(text=get_locale_text(lang, "clear_cart")),
        KeyboardButton(text=get_locale_text(lang, "main_menu"))
    )

    markup.row(
        KeyboardButton(text=get_locale_text(lang, "checkout"))
    )
    return markup
