from telegram.ext import Application, MessageHandler, CommandHandler, filters
import os
import logging
from telegram.request import HTTPXRequest

TOKEN = ""
TELEGRAM_ALLOWED_CHAT_IDS = []
# only these extensions (lower‑case) are allowed
ALLOWED_EXT = {
    '.doc', '.docx',
    '.xls', '.xlsx',
    '.ppt', '.pptx',
    '.pdf',
    '.jpeg', '.jpg',
    '.bmp', '.gif', '.png', '.tiff'
}
http_request = HTTPXRequest(
    connect_timeout=60.0,  # seconds to establish TCP connection
    read_timeout=120.0,    # seconds to download the file
)
async def print_file(update, context):
    if (chat_id := update.message.chat_id) not in TELEGRAM_ALLOWED_CHAT_IDS:
        logging.warning(f"Chat {str(chat_id)} not allowed")
        await update.message.reply_text("🚫 " + _("chat_not_allowed", str(chat_id)))
        return
    msg = update.message

    # 1) document case
    if msg.document:
        name = msg.document.file_name
        file_obj = await msg.document.get_file()

    # 2) photo case (Telegram strips filename, but we know it's a JPG)
    elif msg.photo:
        # pick the highest-res photo
        photo = msg.photo[-1]
        name = f"{photo.file_unique_id}.jpg"
        file_obj = await photo.get_file()

    else:
        # neither doc nor photo
        return await msg.reply_text("🚫 No document or photo found.")

    # extract & check extension
    _, ext = os.path.splitext(name)
    ext = ext.lower()
    if ext not in ALLOWED_EXT:
        return await msg.reply_text(
            f"❌ Unsupported file type: `{ext}`\n"
            "Allowed: " + ", ".join(sorted(ALLOWED_EXT)),
            parse_mode="Markdown"
        )

    # download, print, reply
    local = os.path.join('/tmp', name)
    await file_obj.download_to_drive(local)
    os.system(f'lp "{local}"')
    await msg.reply_text(f'✅ Printing initiated: `{name}`', parse_mode="Markdown")

async def start(update, context):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is {chat_id}")

def main():
    application = Application.builder().token(TOKEN).request(http_request).build()
    application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, print_file))
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
