import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.request import HTTPXRequest
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    CommandHandler,
    filters
)

load_dotenv(override=True)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ALLOWED_CHAT_IDS = os.getenv("TELEGRAM_ALLOWED_CHAT_IDS", "").split(",")
ALLOWED_EXT = {
    '.doc', '.docx',
    '.xls', '.xlsx',
    '.ppt', '.pptx',
    '.pdf',
    '.jpeg', '.jpg',
    '.bmp', '.gif', '.png', '.tiff'
}
HTTP_REQUEST = HTTPXRequest(
    connect_timeout=60.0,  # seconds to establish TCP connection
    read_timeout=120.0,    # seconds to download the file
)

def check_allowed_chat_id(update: Update) -> bool:
    """
    Checks if the chat ID of the update is in the allowed list.

    Args:
        update: The update object containing the message.

    Returns:
        bool: True if the chat ID is allowed, False otherwise.
    """
    chat_id = str(update.message.chat_id)
    return chat_id in TELEGRAM_ALLOWED_CHAT_IDS

async def download_file(msg) -> str:
    """
    Downloads the file sent in the update and returns the file path.

    Args:
        update: The update object containing the message.

    Returns:
        str: The path to the downloaded file.
    """
    if msg.document:
        file_name = msg.document.file_name
        file_obj = await msg.document.get_file()
    elif msg.photo:
        photo = msg.photo[-1]  # Get the highest resolution photo
        file_name = f"{photo.file_unique_id}.jpg"
        file_obj = await photo.get_file()
    else:
        return None

    _, ext = os.path.splitext(file_name)
    ext = ext.lower()
    if ext not in ALLOWED_EXT:
        return None
    
    local = os.path.join("/tmp", file_name)
    await file_obj.download_to_drive(local)

    return local

def print_file(local_file_name: str) -> None:
    """
    Prints the file using the system's default print command.

    Args:
        local_file_name: The path to the file to be printed.
    """
    os.system(f"lp {local_file_name}")

async def print_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Prints any file sent to the bot with a allowed extension.

    Args:
        update: The update object containing the message.
        context: The context object for the bot.
    """
    if not check_allowed_chat_id(update):
        logging.warning(f"Unauthorized chat ID: {update.message.chat_id}")
        await update.message.reply_text(
            "You are not authorized to use this bot."
        )

    msg = update.message
    local_file_name = await download_file(msg)

    if not local_file_name:
        return

    print_file(local_file_name)
    await msg.reply_text(f'✅ Printing initiated: `{local_file_name}`', parse_mode="Markdown")

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Checks the chat ID of the user, for adding it to the allowed list.
    """
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is {chat_id}")

def main():
    """
    Main function to start the Telegram bot application.
    """
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).request(HTTP_REQUEST).build()
    application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, print_file_handler))
    application.add_handler(CommandHandler("start", start_handler))
    application.run_polling()

if __name__ == "__main__":
    main()