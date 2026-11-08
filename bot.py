import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession

TOKEN = "9259216256:AAGAWNQexWsQ38CxjaPVx1bi9Hh8mf28I7c" 

logging.basicConfig(level=logging.INFO)
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Нажми /menu, чтобы увидеть кнопки.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Доступные команды:\n/start\n/help\n/menu")


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Привет"))
    builder.add(types.KeyboardButton(text="Время"))
    builder.add(types.KeyboardButton(text="Помощь"))
    builder.adjust(3) # кнопки в один ряд
    
    await message.answer(
        "Вот главное меню (кнопки внизу):",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.message(Command("inline"))
async def cmd_inline(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Перейти на сайт", url="https://ya.ru"))
    builder.add(types.InlineKeyboardButton(text="Поделиться", callback_data="share"))
    
    await message.answer("Вот инлайн-кнопки:", reply_markup=builder.as_markup())


@dp.message(F.text == "Привет")
async def btn_hello(message: types.Message):
    await message.answer("И тебе привет!")

@dp.message(F.text == "Время")
async def btn_time(message: types.Message):
    now = datetime.now().strftime("%H:%M:%S")
    await message.answer(f"Текущее время: {now}")

@dp.message(F.text == "Помощь")
async def btn_help(message: types.Message):
    await message.answer("Это кнопка помощи. Введи /inline, чтобы увидеть другие кнопки.")


@dp.callback_query(F.data == "share")
async def process_share(callback: types.CallbackQuery):
    await callback.answer("Ура, ты поделился!") 
    await callback.message.edit_text("Спасибо, что поделился!") 

async def main():
    print("Бот с кнопками запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())