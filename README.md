# Telegram Printer Bot
This is a Telegram bot that allows users to print documents and images directly from their Telegram chats. It requires to run on a machine with the default `lp` command available (typically a Linux machine with CUPS installed). The bot does not support configuration through the Telegram interface, you will need to edit the code if you want to do `lp -n 3 -o fit-to-page osition=top-left document.pdf` or similar.

## How to Use
1. Make sure your machine's printer works with the `lp` command by installing printer drivers and CUPS.
    - Install and configure CUPS (Common UNIX Printing System):
        ```bash
        sudo apt install cups
        sudo usermod -a -G lpadmin user  # Replace "user" with your username
        sudo systemctl restart cups
        ```
    - test the printer:
        ```bash
        lp somefile.pdf
        ```
2. Clone this repository
    ```bash
    git clone https://github.com/joeyHXD/telegram_printer_bot
    cd telegram_printer_bot
    ```
3. Setup Environment
   - [UV's installation guide](https://docs.astral.sh/uv/getting-started/installation/) [You can also install the dependencies inside pyproject.toml using venv or conda, if you prefer that]
    ```bash
    uv sync
    ```
4. Copy the `.env.example` file to `.env` and setup your Telegram bot token and allowed chat IDs:
    ```bash
    cp .env.example .env
    ```
    - Get your bot token from [BotFather](https://t.me/botfather) on Telegram.
    - If you don't know your chat ID, you can start the bot and it will reply with your chat ID. You can also use the `/start` command to get your chat ID. Then you might want to add it to the `.env` file under `TELEGRAM_ALLOWED_CHAT_IDS` and **restart the bot**.
5. Run the bot
    ```bash
    uv run app.py
    ```