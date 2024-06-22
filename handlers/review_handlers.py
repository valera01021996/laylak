from config import bot, dp, ADMINS
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from database.tools import DBTools
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.review_keyboards import generate_cancel
from keyboards.main_menu_keyboards import get_main_menu_keyboard
from test import get_locale_text


class Review(StatesGroup):
    full_name = State()
    phone_number = State()
    review = State()


@dp.message_handler(lambda message: message.text in ["✍   Оставить отзыв", "✍   Leave Feedback", "✍   Otzyv"])
async def leave_review(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    await bot.send_message(chat_id, get_locale_text(lang, "review_message"))
    await request_full_name(message, lang)


@dp.message_handler(state=Review.full_name)
async def check_full_name(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    full_name = message.text
    full_name_list = full_name.split()
    if len(full_name_list) == 3:
        for word in full_name_list:
            if not word.isalpha():
                await bot.send_message(chat_id, get_locale_text(lang, "full_name_letter"))
                return

        async with state.proxy() as data:
            data["full_name"] = full_name

        await request_phone_number(message, lang)
        await Review.next()
    elif message.text in ["Cancel", "Отменить", "Bekor qilish"]:
        await state.reset_state(with_data=False)
        await bot.send_message(chat_id, get_locale_text(lang, "main_menu"), reply_markup=get_main_menu_keyboard(lang))
    else:
        await bot.send_message(chat_id, get_locale_text(lang, "full_name_required"))


@dp.message_handler(state=Review.phone_number)
async def check_phone_number(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    phone_number = message.text
    if phone_number.startswith("+") and len(phone_number[1:]) == 12 and phone_number[1:].isdigit():
        async with state.proxy() as data:
            data["phone_number"] = phone_number
        await request_review(message, lang)
        await Review.next()
    elif message.text in ["Cancel", "Отменить", "Bekor qilish"]:
        await state.reset_state(with_data=False)
        await bot.send_message(chat_id, get_locale_text(lang, "main_menu"), reply_markup=get_main_menu_keyboard(lang))
    else:
        await bot.send_message(chat_id, get_locale_text(lang, "invalid_phone_number"))


@dp.message_handler(state=Review.review)
async def leave_review(message: Message, state: FSMContext):
    lang = (await state.get_data()).get('lang', 'en')
    chat_id = message.chat.id
    review = message.text
    async with state.proxy() as data:
        data["review"] = review
    if message.text in ["Cancel", "Отменить", "Bekor qilish"]:
        await state.reset_state(with_data=False)
        await bot.send_message(chat_id, get_locale_text(lang, "main_menu"), reply_markup=get_main_menu_keyboard(lang))
    else:
        await  save_review(chat_id, state)
        await message.answer(get_locale_text(lang, "thanks_feedback"), reply_markup=get_main_menu_keyboard(lang))
        text = await formatted_message(state)
        for admin_id in ADMINS:
            await bot.send_message(admin_id, text)
        await state.finish()


async def request_full_name(message: Message, lang):
    chat_id = message.chat.id
    await bot.send_message(chat_id, get_locale_text(lang, "enter_full_name"), reply_markup=generate_cancel(lang))
    await Review.full_name.set()


async def request_phone_number(message: Message, lang):
    chat_id = message.chat.id
    await bot.send_message(chat_id, get_locale_text(lang, "enter_phone_number"), reply_markup=generate_cancel(lang))


async def request_review(message: Message, lang):
    chat_id = message.chat.id
    await bot.send_message(chat_id, get_locale_text(lang, "leave_review"), reply_markup=generate_cancel(lang))


async def save_review(chat_id, state: FSMContext):
    user_id = DBTools().user_tools.get_user_id(chat_id)
    async with state.proxy() as data:
        DBTools().review_tools.save_review(
            user_id,
            data["full_name"],
            data["phone_number"],
            data["review"]
        )


async def formatted_message(state: FSMContext):
    async with state.proxy() as data:
        return f"Новый отзыв ❗❗❗ \n" \
               f"От пользователя: {data['full_name']}\n" \
               f"Номер телефона: {data['phone_number']}\n" \
               f"Отзыв: {data['review']}"