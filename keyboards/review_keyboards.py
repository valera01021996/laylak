from aiogram.types.reply_keyboard import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
from test import get_locale_text


def generate_cancel(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text=get_locale_text(lang, "cancel"))
    )
    return markup
