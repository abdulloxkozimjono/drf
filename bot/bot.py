import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8396342724:AAEm9AGB9_HVNxlgMk-4yQ2spqwXsHNP3Vs"
API_CREATE_URL = "http://127.0.0.1:8000/api/orders/create/"
API_LIST_URL = "http://127.0.0.1:8000/api/orders/user/"  # foydalanuvchi zakaslarini olish uchun

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}  # user_id -> buyurtma ma'lumotlari


# /start komandasi
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📦 Mahsulotlar")],
            [types.KeyboardButton(text="🛒 Mening zakaslarim")]
        ],
        resize_keyboard=True
    )
    await message.answer("Assalomu alaykum! Tanlang:", reply_markup=kb)


# Mahsulotlar tugmasi
@dp.message(lambda m: m.text == "📦 Mahsulotlar")
async def show_products(message: types.Message):
    # Misol mahsulotlar
    products = [
        {"id": 1, "name": "Mahsulot 1", "desc": "Tavsif 1", "price": 100, "qty": 5},
        {"id": 2, "name": "Mahsulot 2", "desc": "Tavsif 2", "price": 200, "qty": 3},
        {"id": 3, "name": "Mahsulot 3", "desc": "Tavsif 3", "price": 150, "qty": 10},
    ]

    for p in products:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Buyurtma berish", callback_data=f"order_{p['id']}")]]
        )
        await message.answer(f"📌 {p['name']}\n📝 {p['desc']}\n💰 Narxi: {p['price']}\n📦 Soni: {p['qty']}",
                             reply_markup=kb)


# Mening zakaslarim tugmasi
@dp.message(lambda m: m.text == "🛒 Mening zakaslarim")
async def my_orders(message: types.Message):
    user_id = message.from_user.id
    # DRF API dan foydalanuvchining zakaslarini olish
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_LIST_URL}{user_id}/") as resp:
            if resp.status == 200:
                orders = await resp.json()
                if orders:
                    text = "🛒 Sizning zakaslaringiz:\n\n"
                    for o in orders:
                        text += f"📌 Mahsulot: {o['product_name']}\n💰 Narx: {o['product_price']}\n📦 Soni: {o['quantity']}\n\n"
                    await message.answer(text)
                else:
                    await message.answer("🛑 Sizning zakaslaringiz mavjud emas")
            else:
                await message.answer("❌ Zakalarni olishda xatolik yuz berdi")


# Buyurtma tugmasi bosilganda
@dp.callback_query(lambda c: c.data.startswith("order_"))
async def order_callback(call: types.CallbackQuery):
    product_id = int(call.data.split("_")[1])
    user_data[call.from_user.id] = {"product_id": product_id, "step": "phone"}

    contact_button = KeyboardButton(text="📞 Telefon raqam yuborish", request_contact=True)
    kb = ReplyKeyboardMarkup(keyboard=[[contact_button]], resize_keyboard=True)

    await call.message.answer("📞 Iltimos, telefon raqamingizni yuboring:", reply_markup=kb)
    await call.answer()


# Telefon raqam qabul qilish
@dp.message(lambda m: m.contact)
async def get_contact(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.contact.phone_number
    user_data[message.from_user.id]["step"] = "address"
    await message.answer("📍 Iltimos, manzilingizni yuboring:")


# Manzil qabul qilish va API ga yuborish
@dp.message(lambda m: m.text and user_data.get(m.from_user.id, {}).get("step") == "address")
async def get_address(message: types.Message):
    user_data[message.from_user.id]["address"] = message.text
    data = {
        "product": user_data[message.from_user.id]["product_id"],
        "quantity": 1,  # default 1 ta mahsulot
        "phone": user_data[message.from_user.id]["phone"],
        "address": user_data[message.from_user.id]["address"],
        "user_id": message.from_user.id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_CREATE_URL, json=data) as resp:
            if resp.status == 201:
                await message.answer("✅ Buyurtma qabul qilindi!")
            else:
                err = await resp.json()
                await message.answer(f"❌ Xatolik: {err}")

    # Stepni tozalash
    user_data.pop(message.from_user.id, None)


# Botni ishga tushirish
async def start_bot():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
