# telegram_bot.py
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
from config import TELEGRAM_TOKEN, CHAT_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)
        self.updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
        self.setup_handlers()

    def setup_handlers(self):
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("estado", self.status))

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "🚀 Bot de detección de gemas Solana activado!\n"
            "Comandos disponibles:\n"
            "/start - Iniciar el bot\n"
            "/estado - Ver estadísticas"
        )

    def status(self, update: Update, context: CallbackContext):
        from db import get_token_count
        count = get_token_count()
        update.message.reply_text(
            f'📊 Estado del bot:\n'
            f'Tokens detectados: {count}\n'
            f'Chat ID: {CHAT_ID}'
        )

    def send_alert(self, token_data):
        try:
            message = (
                f"🚀 Nuevo token filtrado:\n\n"
                f"Nombre: {token_data['name']}\n"
                f"Precio: ${token_data['price']:.8f}\n"
                f"Volumen 24h: ${token_data['volume']:,.2f}\n"
                f"TX (24h): {token_data['tx_count']}\n"
                f"🔗 [Ver en Dexscreener]({token_data['url']})"
            )
            
            self.bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Error enviando alerta: {str(e)}")

    def run(self):
        self.updater.start_polling()
        logger.info("Bot de Telegram iniciado")
        self.updater.idle()

# Inicialización del bot
try:
    telegram_bot = TelegramBot()
except Exception as e:
    logger.critical(f"Error inicializando bot de Telegram: {str(e)}")
    raise