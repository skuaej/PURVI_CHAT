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
        "Use /langs to see available language codes. "
        "Use /tr <language_code> <text> to translate specific text (e.g., /tr fr Hello)."
    )

async def langs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List available language codes."""
    lang_list = "\n".join([f"{code}: {name}" for code, name in LANGUAGES.items()])
    await update.message.reply_text(f"Available languages:\n{lang_list}")

async def setlang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set the target language for translations."""
    user_id = update.message.from_user.id
    args = context.args

    if not args:
        await update.message.reply_text("Please provide a language code. E.g., /setlang fr")
        return

    lang_code = args[0].lower()
    if lang_code not in LANGUAGES:
        await update.message.reply_text("Invalid language code. Use /langs to see available codes.")
        return

    user_languages[user_id] = lang_code
    await update.message.reply_text(f"Target language set to {LANGUAGES[lang_code]} ({lang_code}).")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Translate incoming text messages to the user's preferred language."""
    user_id = update.message.from_user.id
    text = update.message.text
    target_lang = user_languages.get(user_id, 'en')  # Default to English

    try:
        translated = translator.translate(text, dest=target_lang)
        await update.message.reply_text(f"Translation ({LANGUAGES[target_lang]}): {translated.text}")
    except Exception as e:
        logger.error(f"Translation error: {e}")
        await update.message.reply_text("Error during translation. Please try again.")

async def tr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Translate text to a specific language using /tr <language_code> <text>."""
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /tr <language_code> <text> (e.g., /tr fr Hello)")
        return

    lang_code = args[0].lower()
    if lang_code not in LANGUAGES:
        await update.message.reply_text("Invalid language code. Use /langs to see available codes.")
        return

    text = ' '.join(args[1:])
    try:
        translated = translator.translate(text, dest=lang_code)
        await update.message.reply_text(f"Translation ({LANGUAGES[lang_code]}): {translated.text}")
    except Exception as e:
        logger.error(f"Translation error: {e}")
        await update.message.reply_text("Error during translation. Please try again.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("An error occurred. Please try again.")

def main() -> None:
    """Run the bot."""
    # Replace 'YOUR_BOT_TOKEN_HERE' with your actual Telegram bot token obtained from BotFather
    BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("langs", langs))
    application.add_handler(CommandHandler("setlang", setlang))
    application.add_handler(CommandHandler("tr", tr))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
