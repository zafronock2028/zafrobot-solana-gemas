# telegram_bot.py
import os
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
        self._validate_credentials()
        self.bot = Bot(token=TELEGRAM_TOKEN)
        self.updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
        self._setup_handlers()
        logger.info("Bot inicializado correctamente")

    def _validate_credentials(self):
        """Valida las credenciales esenciales antes de inicializar"""
        if not TELEGRAM_TOKEN:
            raise RuntimeError("TELEGRAM_TOKEN no está configurado en variables de entorno")
        if not CHAT_ID:
            raise RuntimeError("CHAT_ID no está configurado en variables de entorno")

    def _setup_handlers(self):
        """Configura los manejadores de comandos"""
        handlers = [
            CommandHandler("start", self._start),
            CommandHandler("estado", self._status)
        ]
        for handler in handlers:
            self.updater.dispatcher.add_handler(handler)

    def _start(self, update: Update, context: CallbackContext):
        """Manejador del comando /start"""
        update.message.reply_text(
            "🚀 Bot de detección de gemas Solana activado!\n"
            "Comandos disponibles:\n"
            "/start - Mostrar este mensaje\n"
            "/estado - Ver estadísticas del bot"
        )

    def _status(self, update: Update, context: CallbackContext):
        """Manejador del comando /estado"""
        from db import get_token_count
        count = get_token_count()
        update.message.reply_text(
            f'📊 Estado actual:\n'
            f'• Tokens detectados: {count}\n'
            f'• Último escaneo: {self._get_last_scan()}'
        )

    def send_alert(self, token_data):
        """Envía alertas de nuevos tokens detectados"""
        try:
            message = self._format_alert_message(token_data)
            self.bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Error enviando alerta: {str(e)}")

    def _format_alert_message(self, token_data):
        """Formatea el mensaje de alerta"""
        return (
            f"🚀 **Nuevo token detectado!**\n\n"
            f"• Nombre: `{token_data['name']}`\n"
            f"• Precio: ${token_data['price']:.8f}\n"
            f"• Volumen 24h: ${token_data['volume']:,.2f}\n"
            f"• Transacciones (24h): {token_data['tx_count']}\n"
            f"• [Ver en Dexscreener]({token_data['url']})"
        )

    def _get_last_scan(self):
        """Obtiene la hora del último escaneo (implementar lógica real)"""
        return "Hace 30 segundos"

    def run(self):
        """Inicia el bot"""
        self.updater.start_polling()
        logger.info("Bot iniciado y escuchando comandos")
        self.updater.idle()

# Inicialización segura con manejo de errores
try:
    telegram_bot = TelegramBot()
except Exception as init_error:
    logger.critical(f"Error crítico durante inicialización: {str(init_error)}")
    raise