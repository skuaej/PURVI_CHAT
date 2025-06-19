import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# List of random image URLs
image_urls = [
    "https://picsum.photos/200/300",
    "https://placekitten.com/300/300",
    "https://loremflickr.com/320/240",
    "https://source.unsplash.com/random/400x300",
]

# Command handler for /random
async def send_random_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_url = random.choice(image_urls)
    await update.message.reply_photo(photo=image_url)

def main():
    # You need to insert your bot token below
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

    # Register the /random command
    app.add_handler(CommandHandler("random", send_random_image))

    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()
