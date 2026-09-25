import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

PRODUCTS = {
    "1": {
        "name": "Цифровой товар №1",
        "description": "Описание товара",
        "price": 100
    },
    "2": {
        "name": "Цифровой товар №2",
        "description": "Описание товара",
        "price": 200
    }
}


@dp.message(Command("start"))
async def start(message: Message):
    text = "🛒 Добро пожаловать!\n\n"

    for number, product in PRODUCTS.items():
        text += (
            f"🔹 {number}. {product['name']}\n"
            f"💫 Цена: {product['price']} Stars\n\n"
        )

    text += "Для покупки отправь номер товара."

    await message.answer(text)


@dp.message(F.text.in_(PRODUCTS))
async def buy(message: Message):
    product = PRODUCTS[message.text]

    await bot.send_invoice(
        chat_id=message.chat.id,
        title=product["name"],
        description=product["description"],
        payload=f"product_{message.text}",
        currency="XTR",
        prices=[
            LabeledPrice(
                label=product["name"],
                amount=product["price"]
            )
        ]
    )


@dp.pre_checkout_query()
async def checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)


@dp.message(F.successful_payment)
async def payment(message: Message):
    await message.answer(
        "✅ Оплата получена!\n\n"
        "Спасибо за покупку! 💫"
    )


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
