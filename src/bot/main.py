import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from .deadlines_service import format_deadlines, get_deadlines

load_dotenv()

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я StudyPulse — помогу не пропускать дедлайны.")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/add — добавить дедлайн\n"
        "/deadlines — список дедлайнов\n"
        "/habits — привычки\n"
        "/stats — статистика"
    )


@dp.message(Command("deadlines"))
async def cmd_deadlines(message: Message):
    deadlines = get_deadlines(message.from_user.id)
    await message.answer(format_deadlines(deadlines))


async def main():
    bot = Bot(token=os.environ["BOT_TOKEN"])
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
