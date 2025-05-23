import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator, LANGUAGES

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize translator
translator = Translator()

# Store user language preferences
user_languages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text(
        "Welcome to the Translator Bot! Send any text to translate it to English (default). "
        "Use /setlang <language_code> to change the target language (e.g., /setlang fr for French). "
        "Use /langs to see available language codes."
    )

async def langs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List available language codes."""
    lang_list = "\n".join([f"{code}: {name
