# telegram_bot.py
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, CHAT_ID
from db import get_token_count

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Bot de detección de gemas Solana activado!\n"
        "Comandos disponibles:\n"
        "/start - Mostrar este mensaje\n"
        "/estado - Ver estadísticas del bot"
    )

async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = get_token_count()
    await update.message.reply_text(
        f'📊 Tokens detectados: {count}'
    )

def send_alert(token_data):
    try:
        message = (
            f"🚀 *Nuevo token detectado!*\n\n"
            f"*Nombre:* `{token_data['name']}`\n"
            f"*Precio:* ${token_data['price']:.8f}\n"
            f"*Volumen 24h:* ${token_data['volume']:,.2f}\n"
            f"*Transacciones:* {token_data['tx_count']}\n"
            f"[Ver en Dexscreener]({token_data['url']})"
        )
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error al enviar alerta: {e}")

def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("estado", estado))
    logger.info("Bot de Telegram iniciado con éxito")
    app.run_polling()