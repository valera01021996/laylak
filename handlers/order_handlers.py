from find_address import get_address_via_coords
from database.tools import DBTools
from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters import Text
from database.tools import DBTools
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.order_keyboards import *
from keyboards.main_menu_keyboards import get_main_menu_keyboard
from config import bot, dp, ADMINS


class OrderForm(StatesGroup):
    cart_id = State()
    location = State()
    phone_number = State()
    confirm = State()


@dp.message_handler(
    lambda message: message.text in ["🚖   Checkout", "🚖   Оформить заказ", "🚖   Ro'yxatdan o'chirilish"])
async def create_order(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    print("WORKING !")
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    await bot.send_message(chat_id, get_locale_text(lang, "checkout_text"),
                           reply_markup=generate_request_location_menu(lang))
    await OrderForm.location.set()


@dp.message_handler(state=OrderForm.location, content_types=ContentType().LOCATION)
async def check_location(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    async with state.proxy() as data:
        data["location"] = {
            "latitude": message.location.latitude,
            "longitude": message.location.longitude
        }
        await bot.send_message(chat_id, get_locale_text(lang, "send_phone_number"),
                               reply_markup=generate_request_contact_menu(lang))
        await OrderForm.phone_number.set()
#
#
@dp.message_handler(state=OrderForm.phone_number, content_types=ContentType().CONTACT)
async def check_phone_number(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    confirm_text = await formatted_message_for_confirm(data, cart_id, phone_number, lang)
    await OrderForm.confirm.set()
    await bot.send_message(chat_id, confirm_text, reply_markup=generate_confirm_menu(lang))
#
#
@dp.message_handler(state=OrderForm.confirm)
async def success_confirm(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    data = await state.get_data()
    chat_id = message.chat.id
    full_name = message.chat.full_name
    user_id = DBTools().user_tools.get_user_id(chat_id)
    cart_id = DBTools().cart_tools.get_active_cart(user_id)[0]
    cart_products = DBTools().cart_tools.get_cart_products(cart_id)
    if message.text in ["Yes", "Да", "Ha"]:
        await state.finish()
        text_admins = await formatted_message_for_admins(data, full_name, cart_products, lang)
        await bot.send_message(chat_id, get_locale_text(lang, 'confirm_message'), reply_markup=get_main_menu_keyboard(lang))
        for admin_id in ADMINS:
            await bot.send_message(admin_id, text_admins)
            await bot.send_location(admin_id, latitude=data["location"]["latitude"],
                                    longitude=data["location"]["longitude"])
        DBTools().order_tools.create_order(cart_id)
        DBTools().cart_tools.change_order_status(cart_id)
        DBTools().cart_tools.register_cart(user_id)
    else:
        await message.answer(get_locale_text(lang, 'order_cancelled'), reply_markup=get_main_menu_keyboard(lang))
        await state.reset_state(with_data=False)
#
#
@dp.message_handler(state=OrderForm.location)
async def check_location(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = (await state.get_data()).get('lang', 'en')
    if message.text in ["Cancel", "Отменить", "Bekor qilish"]:
        await state.reset_state(with_data=False)
        await bot.send_message(chat_id, get_locale_text(lang, 'main_menu'), reply_markup=get_main_menu_keyboard(lang))


@dp.message_handler(state=OrderForm.phone_number)
async def check_location(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = (await state.get_data()).get('lang', 'en')
    if message.text in ["Cancel", "Отменить", "Bekor qilish"]:
        await state.reset_state(with_data=False)
        await bot.send_message(chat_id, get_locale_text(lang, 'main_menu'), reply_markup=get_main_menu_keyboard(lang))
#
#
async def formatted_message_for_confirm(data, cart_id, phone_number, lang):
    address = await get_address(data, lang)
    confirm = f"{get_locale_text(lang, 'order_number')} {cart_id}\n" \
              f"{get_locale_text(lang, 'order_address')} {address}\n" \
              f"{get_locale_text(lang, 'order_phone_number')} {phone_number}\n\n"
    total = int()
    cart_products = DBTools().cart_tools.get_cart_products(cart_id)
    i = 0
    for _, title, quantity, total_coast in cart_products:
        i += 1
        total += total_coast
        confirm += f"    {i}.{title}\n" \
                   f"      {get_locale_text(lang, 'quantity')} {quantity} {get_locale_text(lang, 'piece')}.\n" \
                   f"      {get_locale_text(lang, 'cost')} {total_coast} {get_locale_text(lang, 'currency')}. \n\n"
    last_message = confirm + get_locale_text(lang, 'total') + ":" + " " + str(total) + " " + get_locale_text(lang, 'currency')
    return last_message
#
#
async def get_address(data, lang):
    longitude = str(data['location']['longitude'])
    latitude = str(data['location']['latitude'])
    coords = longitude + ',' + latitude
    address = await get_address_via_coords(coords, lang)
    return address
#
#
async def formatted_message_for_admins(data, full_name: str, cart_products: list, lang):
    address = await get_address(data, lang)
    text = f"Новый заказ !\n" \
           f"От пользователя: {full_name}\n" \
           f"Адрес: {address}\n\n" \
           f"Номер телефона: {data['phone_number']}\n\n"
    i = 0
    total = int()
    for _, title, quantity, total_coast in cart_products:
        i += 1
        total += total_coast
        text += f"    {i}.{title}\n" \
                f"      Количество: {quantity} шт.\n" \
                f"      Стоимость: {total_coast} сум. \n\n"
    last_message = text + "Итого: " + str(total) + "сум"
    return last_message

