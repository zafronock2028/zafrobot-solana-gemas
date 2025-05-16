import asyncio
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from db import get_token_count

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == CHAT_ID:
        await context.bot.send_message(chat_id=CHAT_ID, text="🚀 Bot activo\nComandos:\n/start - Bienvenida\n/estado - Tokens detectados")

async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == CHAT_ID:
        count = get_token_count()
        await context.bot.send_message(chat_id=CHAT_ID, text=f"📊 Tokens guardados en la base de datos: {count}")

async def run_bot_async():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("estado", estado))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    # Mantén el bot activo sin cerrar el loop
    while True:
        await asyncio.sleep(3600)

def run_bot():
    asyncio.run(run_bot_async())

def send_alert(token):
    bot = Bot(token=BOT_TOKEN)
    msg = f"🚨 Joya detectada: {token['name']}\n💵 Precio: ${token['price']}\n📈 Volumen: ${token['volume']}\n👥 Holders: {token['holders']}\n🔗 Enlace: {token['url']}"
    bot.send_message(chat_id=CHAT_ID, text=msg)