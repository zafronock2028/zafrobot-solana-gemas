from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, CHAT_ID
from db import get_token_count
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)
        self.app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        self.app.add_handler(CommandHandler("start", self._start))
        self.app.add_handler(CommandHandler("estado", self._status))
        logger.info("Bot de Telegram inicializado")

    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🚀 Bot activo\nComandos:\n/start - Bienvenida\n/estado - Tokens detectados"
        )

    async def _status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        count = get_token_count()
        await update.message.reply_text(
            f'📊 Tokens guardados en la base de datos: {count}'
        )

    def send_alert(self, token_data):
        try:
            message = (
                f"🚀 *Nuevo token detectado!*\n\n"
                f"• Nombre: `{token_data['name']}`\n"
                f"• Precio: ${token_data['price']:.8f}\n"
                f"• Volumen: ${token_data['volume']:,.2f}\n"
                f"• Transacciones: {token_data['tx_count']}\n"
                f"[Ver en Dexscreener]({token_data['url']})"
            )
            self.bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Error al enviar alerta: {e}")

    def run(self):
        self.app.run_polling()

telegram_bot = TelegramBot()