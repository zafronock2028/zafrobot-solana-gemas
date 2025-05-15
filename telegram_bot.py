# telegram_bot.py
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('🚀 Bot de detección de gemas Solana activado!')

def status(update: Update, context: CallbackContext):
    from db import get_token_count
    count = get_token_count()
    update.message.reply_text(f'📊 Estado del bot:\nTokens detectados: {count}')

def send_alert(token):
    message = f"""🚀 Nuevo token filtrado:

Nombre: {token['name']}  
Precio: ${token['price']}  
Volumen 24h: ${token['volume']:,.2f}  
TX (24h): {token['tx_count']}  
🔗 [Ver en Dexscreener]({token['url']})"""
    
    bot.send_message(
        chat_id=CHAT_ID,
        text=message,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

def setup_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("estado", status))

def start_bot():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    setup_dispatcher(updater.dispatcher)
    updater.start_polling()
    logger.info("Bot de Telegram iniciado")
    updater.idle()