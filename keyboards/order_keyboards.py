from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from test import get_locale_text


def generate_request_contact_menu(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text=get_locale_text(lang, "send_contact"), request_contact=True)
    )
    markup.row(KeyboardButton(text=get_locale_text(lang, "cancel")))
    return markup


def generate_request_location_menu(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text=get_locale_text(lang, "send_location"), request_location=True)
    )
    markup.row(KeyboardButton(text=get_locale_text(lang, "cancel")))
    return markup


def generate_confirm_menu(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        KeyboardButton(text=get_locale_text(lang, "yes"))
    )
    markup.row(
        KeyboardButton(text=get_locale_text(lang, "cancel_order"))
    )
    return markup
