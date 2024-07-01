from config import bot, dp
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from test import get_locale_text
from keyboards.main_menu_keyboards import *
from database.tools import DBTools, ProductTools


async def register_user(full_name, chat_id):
    DBTools().user_tools.register_user(full_name, chat_id)


async def register_cart(chat_id):
    user_id = DBTools().user_tools.get_user_id(chat_id)
    DBTools().cart_tools.register_cart(user_id)


@dp.message_handler(commands=["start"], state="*")
async def start_command(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if lang:
        await message.answer(get_locale_text(lang, "main_menu"),
                             reply_markup=get_main_menu_keyboard(lang))
    else:
        await register_user(full_name, chat_id)
        await register_cart(chat_id)
        lang = (await state.get_data()).get('lang', 'uz')
        await message.answer(get_locale_text(lang, 'start'), reply_markup=get_language_keyboard())


@dp.message_handler(lambda message: message.text in ["🇬🇧 English", "🇺🇿 O'zbek", "🇷🇺 Русский"])
async def set_language(message: Message, state: FSMContext):
    lang = message.text.lower()
    if lang == '🇬🇧 english':
        await state.update_data(lang='en')
        lang = 'en'
    elif lang == '🇷🇺 русский':
        await state.update_data(lang='ru')
        lang = 'ru'
    elif lang == '🇺🇿 o\'zbek':
        await state.update_data(lang='uz')
        lang = 'uz'
    else:
        await message.answer("Please choose a language from the keyboard.")
        return

    await message.answer(get_locale_text(lang, 'language_changed'), reply_markup=get_main_menu_keyboard(lang))


@dp.message_handler(lambda message: message.text in ["🏠 Главное меню", "🏠 Main menu", "🏠 Bosh menyu"])
async def main_menu(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    await message.answer(get_locale_text(lang, 'main_menu'), reply_markup=get_main_menu_keyboard(lang))


@dp.message_handler(lambda message: message.text in ["◀ Назад", "◀ Back", "◀ Orqaga"])
async def categories_menu(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    await message.answer(get_locale_text(lang, 'choose_category'), reply_markup=generate_categories_menu(lang))


@dp.message_handler(lambda message: message.text in ["✅ Start Order", "✅ Начать заказ", "✅ Boshlash"])
async def start_order(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    await message.answer(get_locale_text(lang, 'choose_category'), reply_markup=generate_categories_menu(lang))


@dp.message_handler(lambda message: message.text in ProductTools.CATEGORIES)
async def show_products_menu(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    category_name = message.text
    category_id = DBTools().product_tools.get_category_id(category_name, lang)
    await message.answer(get_locale_text(lang, "choose_product"),
                         reply_markup=generate_products_menu(category_id, lang))


@dp.message_handler(lambda message: message.text in ProductTools.PRODUCTS)
async def show_detail_product(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    pk, name, price, image, description = DBTools().product_tools.get_product_detail(message.text, lang)
    with open(image, mode="rb") as photo:
        await bot.send_photo(message.chat.id, photo, caption=f"<b>{name}</b>\n\n"
                                                             f"<i>{get_locale_text(lang, 'cost')}: {price}</i> {get_locale_text(lang, 'currency')}", parse_mode="HTML",
                             reply_markup=generate_detail_product_menu(lang, name))


@dp.callback_query_handler(lambda call: call.data.startswith("action"))
async def edit_count_product(call: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, action, product_name, current_qty = call.data.split("_")
    current_qty = int(current_qty)

    if action == "minus" and current_qty > 0:
        current_qty -= 1

    elif action == "minus" and current_qty <= 0:
        await bot.answer_callback_query(call.id, get_locale_text(lang, 'wrong_quantity_minus'))
        return

    if action == "current":
        await bot.answer_callback_query(call.id, get_locale_text(lang, 'current_quantity'))
        return

    if action == "plus":
        current_qty += 1

    elif action == "plus" and current_qty >= 500:
        await bot.answer_callback_query(call.id, get_locale_text(lang, 'wrong_quantity_plus'))
        return

    await bot.edit_message_reply_markup(chat_id, message_id,
                                        reply_markup=generate_detail_product_menu(lang, product_name, current_qty))


@dp.message_handler(lambda message: message.text in ["⚙️ Настройки", "⚙️ Sozlamalar", "⚙️ Settings"])
async def settings(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    await bot.send_message(chat_id, get_locale_text(lang, "select_action"), reply_markup=generate_settings_menu(lang))


@dp.message_handler(lambda message: message.text in ["Change language", "Изменить язык", "Tilni o'zgartirish"])
async def show_languages(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    await bot.send_message(chat_id, get_locale_text(lang, "choose_language"), reply_markup=get_language_keyboard())
