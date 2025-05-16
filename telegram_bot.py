# telegram_bot.py
import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import TELEGRAM_TOKEN, CHAT_ID
from db import get_token_count

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🚀 Bot activo\nComandos:\n/start - Bienvenida\n/estado - Tokens detectados"
    )

def status(update: Update, context: CallbackContext):
    count = get_token_count()
    update.message.reply_text(f"📊 Tokens guardados en la base de datos: {count}")

def send_alert(token_data):
    try:
        message = (
            f"🚀 *Nuevo token detectado!*\n\n"
            f"*Nombre:* `{token_data['name']}`\n"
            f"*Precio:* ${token_data['price']:.8f}\n"
            f"*Volumen 24h:* ${token_data['volume']:,.2f}\n"
            f"*Transacciones:* {token_data['tx_count']}\n"
            f"[Ver en Pump.fun]({token_data['url']})"
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
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("estado", status))
    logger.info("Bot de Telegram iniciado")
    updater.start_polling()
    updater.idle()