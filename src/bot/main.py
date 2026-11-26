import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv

from .deadlines_service import (
    format_deadlines,
    get_deadlines,
    parse_reminder_time,
    parse_timezone,
    save_remind_time,
    save_timezone,
)

load_dotenv()

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я StudyPulse - помогу не пропускать дедлайны.")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/add - добавить дедлайн\n"
        "/deadlines - список дедлайнов\n"
        "/habits - привычки\n"
        "/stats - статистика\n"
        "/timezone - часовой пояс\n"
        "/remindtime - время напоминаний"
    )


@dp.message(Command("deadlines"))
async def cmd_deadlines(message: Message):
    deadlines = get_deadlines(message.from_user.id)
    await message.answer(format_deadlines(deadlines))


@dp.message(Command("timezone"))
async def cmd_timezone(message: Message, command: CommandObject):
    name = parse_timezone(command.args or "")
    if name is None:
        await message.answer("Не понял часовой пояс. Пример: /timezone Asia/Yekaterinburg")
        return
    save_timezone(message.from_user.id, name)
    await message.answer(f"Часовой пояс сохранён: {name}")


@dp.message(Command("remindtime"))
async def cmd_remindtime(message: Message, command: CommandObject):
    t = parse_reminder_time(command.args or "")
    if t is None:
        await message.answer("Укажите время в формате ЧЧ:ММ. Пример: /remindtime 09:30")
        return
    save_remind_time(message.from_user.id, t)
    await message.answer(f"Напоминать буду в {t:%H:%M}")


async def main():
    bot = Bot(token=os.environ["BOT_TOKEN"])
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
