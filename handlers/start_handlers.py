from config import bot, dp
from aiogram.types import Message
from keyboards.main_menu_keyboards import get_language_keyboard, get_main_menu_keyboard
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from test import get_locale_text
from keyboards.main_menu_keyboards import *
from database.tools import DBTools, ProductTools


@dp.message_handler(commands=["start"], state="*")
async def start_command(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'uz')
    await message.answer(get_locale_text(lang, 'start'), reply_markup=get_language_keyboard())


@dp.message_handler(lambda message: message.text in ["English", "O'zbek", "Русский"])
async def set_language(message: Message, state: FSMContext):
    lang = message.text.lower()
    if lang == 'english':
        await state.update_data(lang='en')
        lang = 'en'
    elif lang == 'русский':
        await state.update_data(lang='ru')
        lang = 'ru'
    elif lang == 'o\'zbek':
        await state.update_data(lang='uz')
        lang = 'uz'
    else:
        await message.answer("Please choose a language from the keyboard.")
        return

    await message.answer(get_locale_text(lang, 'language_changed'), reply_markup=get_main_menu_keyboard(lang))

@dp.message_handler(lambda message: message.text in ["Главное меню", "Main menu", "Glavnoe menyu"])
async def main_menu(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    await message.answer(get_locale_text(lang, 'main_menu'), reply_markup=get_main_menu_keyboard(lang))


@dp.message_handler(lambda message: message.text in ["Назад", "Back", "Orqaga"])
async def categories_menu(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    await message.answer(get_locale_text(lang, 'choose_category'), reply_markup=generate_categories_menu(lang))


@dp.message_handler(lambda message: message.text in ["Start Order", "Начать заказ", "Boshlash"])
async def start_order(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    await message.answer(get_locale_text(lang, 'choose_category'), reply_markup=generate_categories_menu(lang))


@dp.message_handler(lambda message: message.text in ProductTools.CATEGORIES)
async def show_products_menu(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    category_name = message.text
    category_id = DBTools().product_tools.get_category_id(category_name, lang)
    await message.answer(get_locale_text(lang, "choose_product"), reply_markup=generate_products_menu(category_id, lang))


