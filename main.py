import os
from telegram.ext import Application, CommandHandler
from handlers import (
    start,
    help_command,
    ping,
    uptime,
    info,
    joke,
    roll,
    flip,
    rps,
    eight_ball,
    cat,
    dog,
    quote,
    fact,
    weather,
    crypto,
    qr,
    shorten,
    translate,
    calc,
    wiki,
    time,
    poll,
    define,
    pin,
    unpin,
    kick,
    ban,
    mute,
)
from telegram import Update

def main() -> None:
    """Start the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        token = input("Please enter your Telegram bot token: ")

    application = Application.builder().token(token).build()

    # On different commands - add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("uptime", uptime))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("joke", joke))
    application.add_handler(CommandHandler("roll", roll))
    application.add_handler(CommandHandler("flip", flip))
    application.add_handler(CommandHandler("rps", rps))
    application.add_handler(CommandHandler("8ball", eight_ball))
    application.add_handler(CommandHandler("cat", cat))
    application.add_handler(CommandHandler("dog", dog))
    application.add_handler(CommandHandler("quote", quote))
    application.add_handler(CommandHandler("fact", fact))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("crypto", crypto))
    application.add_handler(CommandHandler("qr", qr))
    application.add_handler(CommandHandler("shorten", shorten))
    application.add_handler(CommandHandler("translate", translate))
    application.add_handler(CommandHandler("calc", calc))
    application.add_handler(CommandHandler("wiki", wiki))
    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("poll", poll))
    application.add_handler(CommandHandler("define", define))
    application.add_handler(CommandHandler("pin", pin))
    application.add_handler(CommandHandler("unpin", unpin))
    application.add_handler(CommandHandler("kick", kick))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("mute", mute))

    # Run the bot until you press Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()