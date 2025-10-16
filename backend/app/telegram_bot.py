import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base
from dotenv import load_dotenv

import asyncio

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")  # замени на свой Postgres, если уже настроен

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# SQLAlchemy engine/session
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@dp.message(Command("start"))
async def send_welcome(message: Message):
    async with AsyncSessionLocal() as db:
        tg_id = message.from_user.id
        username = message.from_user.username or ""
        # Проверяем, есть ли пользователь с этим Telegram ID
        result = await db.execute(
            User.__table__.select().where(User.id == tg_id)
        )
        user = result.first()
        if not user:
            # Создаём пользователя с Telegram ID (почта и пароль - заглушки)
            new_user = User(id=tg_id, email=f"{tg_id}@telegram", hashed_password="telegram", full_name=username)
            db.add(new_user)
            await db.commit()
            await message.answer("Добро пожаловать в AI Lifeline! Ваш Telegram аккаунт привязан.")
        else:
            await message.answer("С возвращением в AI Lifeline!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
