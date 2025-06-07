import os
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MOD_GROUP_ID = int(os.getenv("MOD_GROUP_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton("🦷 Запропонувати кейс")],
        [KeyboardButton("📥 Запропонувати контент"), KeyboardButton("❓ Питання та пропозиції")],
        [KeyboardButton("🔍 Пошук колеги")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Привіт! Обери одну з опцій нижче:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text

    if text == "🦷 Запропонувати кейс":
        example = (
            "📌 Приклад оформлення кейсу:\n"
            "— Спеціалізація: ортодонтія\n"
            "— Вік пацієнта: 28 років\n"
            "— Скарги: естетика, скупченість\n"
            "— План лікування: елайнери, IPR\n"
            "— Тривалість: 8 місяців\n"
            "— Результат: покращена естетика, стабільна оклюзія\n\n"
            "📸 Надішли свій кейс у подібному форматі + фото або відео!"
        )
        await message.reply_text(example)

    elif text == "📥 Запропонувати контент":
        await message.reply_text("📩 Надішли свій матеріал (ідеї, статті, шаблони, думки). Ми переглянемо й, можливо, опублікуємо!")

    elif text == "❓ Питання та пропозиції":
        await message.reply_text("🗣 Напиши своє питання або пропозицію — команда dentalPro Hub прочитає кожне повідомлення.")

    elif text == "🔍 Пошук колеги":
        await message.reply_text("🔎 Напиши, кого шукаєш (спеціалізація, місто, формат співпраці). Ми допоможемо знайти потрібну людину.")

    else:
        try:
            await context.bot.copy_message(chat_id=MOD_GROUP_ID, from_chat_id=message.chat_id, message_id=message.message_id)
            await message.reply_text("✅ Дякуємо! Повідомлення передано модераторам.")
        except Exception as e:
            await message.reply_text("⚠️ Сталася помилка при надсиланні. Спробуйте ще раз.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO, handle_message))

app.run_polling()
