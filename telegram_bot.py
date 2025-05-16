# telegram_bot.py
import os
import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import TELEGRAM_TOKEN, CHAT_ID
from db import get_token_count

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializar bot
bot = Bot(token=TELEGRAM_TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🚀 Bot de detección de gemas Solana activado!\n"
        "Comandos disponibles:\n"
        "/start - Mostrar este mensaje\n"
        "/estado - Ver estadísticas del bot"
    )

def status(update: Update, context: CallbackContext):
    count = get_token_count()
    update.message.reply_text(
        f'📊 Estado actual:\n'
        f'• Tokens detectados: {count}\n'
        f'• Último escaneo: hace pocos segundos'
    )

def send_alert(token_data):
    try:
        message = (
            f"🚀 *Nuevo token detectado!*\n\n"
            f"*Nombre:* `{token_data['name']}`\n"
            f"*Precio:* ${token_data['price']:.8f}\n"
            f"*Volumen 24h:* ${token_data['volume']:,.2f}\n"
            f"*Transacciones (24h):* {token_data['tx_count']}\n"
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
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("estado", status))
    logger.info("Bot de Telegram inicializado")
    updater.start_polling()
    updater.idle()