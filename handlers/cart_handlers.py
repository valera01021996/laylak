from config import bot, dp
from aiogram.types import CallbackQuery, Message
from database.tools import DBTools
from aiogram.dispatcher.filters import Text
from test import get_locale_text
from aiogram.dispatcher.storage import FSMContext
from keyboards.cart_keyboards import *
from keyboards.main_menu_keyboards import get_main_menu_keyboard


@dp.callback_query_handler(
    lambda call: call.data.startswith("add-cart")
)
async def add_cart_product(call: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = call.message.chat.id
    _, product_name, current_qty = call.data.split("_")
    current_qty = int(current_qty)
    pk, name, price, _, _ = DBTools().product_tools.get_product_detail(product_name, lang)
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    status_add = DBTools().cart_tools.add_cart_product(cart_id, pk, product_name, current_qty, current_qty * price)

    if status_add:
        await bot.answer_callback_query(call.id, get_locale_text(lang, "product_add"))
    else:
        await bot.answer_callback_query(call.id, get_locale_text(lang, "product_quantity"))


@dp.message_handler(lambda message: message.text in ["🛒 Корзина", "🛒 Cart", "🛒 Savat"])
async def show_cart(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    cart_products = DBTools().cart_tools.get_cart_products(cart_id)
    if not cart_products:
        await bot.send_message(chat_id, get_locale_text(lang, "your_cart_empty"),
                               reply_markup=get_main_menu_keyboard(lang))
    else:
        cart_text = f"<b>{get_locale_text(lang, 'your_cart')}:</b>\n\n"
        total = int()
        i = 0
        for product_id, product_name, quantity, total_coast in cart_products:
            i += 1
            total += total_coast
            cart_text += f"{i}. {product_name}\n" \
                         f"<i>{get_locale_text(lang, 'quantity')}: {quantity} {get_locale_text(lang, 'piece')}</i>\n" \
                         f"<i>{get_locale_text(lang, 'total_cost')}: {total_coast} {get_locale_text(lang, 'currency')}</i>\n\n"
        last_message = f"{cart_text} {get_locale_text(lang, 'total')}:  {str(total)} {get_locale_text(lang, 'currency')}"
        await bot.send_message(chat_id, get_locale_text(lang, 'comment_delete_clear_product'))
        await bot.send_message(chat_id, last_message, parse_mode="HTML",
                               reply_markup=generate_cart_menu_reply_markup(chat_id, lang))


@dp.message_handler(lambda message: message.text.startswith("❌"))
async def delete_product_from_cart(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    product_name = message.text[5:]
    DBTools().cart_tools.delete_product_from_cart(product_name, cart_id)
    cart_products = DBTools().cart_tools.get_cart_products(user_id)
    cart_text = f"<b>{get_locale_text(lang, 'your_cart')}:</b>\n\n"
    total = int()
    i = 0
    for product_id, product_name, quantity, total_coast in cart_products:
        i += 1
        total += total_coast
        cart_text += f"{i}. <b>{product_name}</b>\n" \
                     f"<i>{get_locale_text(lang, 'quantity')}: {quantity} {get_locale_text(lang, 'piece')}</i>\n" \
                     f"<i>{get_locale_text(lang, 'total_cost')}: {total_coast} {get_locale_text(lang, 'currency')}</i>\n\n"
    last_message = f"{cart_text} {get_locale_text(lang, 'total')}:  {str(total)} {get_locale_text(lang, 'currency')}"
    if cart_products:
        await bot.send_message(chat_id, last_message, parse_mode="HTML",
                               reply_markup=generate_cart_menu_reply_markup(chat_id, lang))
    else:
        await bot.send_message(chat_id, get_locale_text(lang, 'main_menu'), reply_markup=get_main_menu_keyboard(lang))


@dp.message_handler(lambda message: message.text.startswith("🔄"))
async def clear_cart(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    DBTools().cart_tools.delete_all_products_from_cart(cart_id)
    await bot.send_message(chat_id, "Ваша корзина очищена", reply_markup=get_main_menu_keyboard(lang))