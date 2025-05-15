# telegram_bot.py
import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
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
        self._setup_handlers()

    def _setup_handlers(self):
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self._start))
        dispatcher.add_handler(CommandHandler("estado", self._status))

    def _start(self, update: Update, context: CallbackContext):
        update.message.reply_text("🚀 Bot de Gemas Solana - Detección temprana de tokens prometedores")

    def _status(self, update: Update, context: CallbackContext):
        from db import get_token_count
        count = get_token_count()
        update.message.reply_text(f'📊 Tokens detectados: {count}')

    def send_alert(self, token_data):
        message = (
            f"🚀 Nuevo token detectado!\n\n"
            f"Nombre: {token_data['name']}\n"
            f"Precio: ${token_data['price']:.8f}\n"
            f"Volumen 24h: ${token_data['volume']:,.2f}\n"
            f"Transacciones: {token_data['tx_count']}\n"
            f"Enlace: {token_data['url']}"
        )
        self.bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

telegram_bot = TelegramBot()