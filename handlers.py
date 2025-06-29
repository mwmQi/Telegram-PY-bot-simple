import random
import re
import wikipedia
import qrcode
from io import BytesIO
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
import httpx
from utils import logger, start_time
from datetime import datetime, timedelta

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcomes the user."""
    await update.message.reply_text("Hi! I am a feature-rich Telegram bot. Send /help to see what I can do.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all available commands."""
    help_text = """
    Available commands:
    /start - Welcomes the user.
    /help - Lists all available commands.
    /ping - Checks if the bot is responsive.
    /uptime - Shows how long the bot has been running.
    /info - Gets information about the user or chat.
    /joke - Tells a random joke.
    /roll <NdS> - Rolls dice (e.g., /roll 2d6).
    /flip - Flips a coin.
    /rps <rock|paper|scissors> - Play Rock, Paper, Scissors.
    /8ball <question> - Ask the magic 8-ball a question.
    /cat - Sends a random picture of a cat.
    /dog - Sends a random picture of a dog.
    /quote - Provides an inspirational quote.
    /fact - Get a random interesting fact.
    /weather <city> - Gets the current weather.
    /crypto <coin> - Gets the latest price of a cryptocurrency (e.g., Bitcoin).
    /qr <text> - Generates a QR code.
    /shorten <url> - Shortens a long URL.
    /translate <lang> <text> - Translates text to a specified language.
    /calc <expression> - A simple calculator.
    /wiki <query> - Searches Wikipedia.
    /time <city> - Gets the current time in a city.
    /poll - Creates a poll in the chat.
    /define <word> - Gets the definition of a word.
    /pin - Pins the message it replies to (admins only).
    /unpin - Unpins the current pinned message (admins only).
    /kick @user - Kicks a user from the group (admins only).
    /ban @user - Bans a user from the group (admins only).
    /mute @user - Mutes a user for a specified time (admins only).
    """
    await update.message.reply_text(help_text)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks if the bot is responsive."""
    await update.message.reply_text("Pong!")

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows how long the bot has been running."""
    now = datetime.now()
    uptime_delta = now - start_time
    await update.message.reply_text(f"Uptime: {uptime_delta}")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gets information about the user or chat."""
    user = update.effective_user
    chat = update.effective_chat
    info_text = (
        f"User ID: {user.id}\n"
        f"First Name: {user.first_name}\n"
        f"Last Name: {user.last_name or 'N/A'}\n"
        f"Username: @{user.username or 'N/A'}\n"
        f"Chat ID: {chat.id}\n"
        f"Chat Type: {chat.type}"
    )
    await update.message.reply_text(info_text)

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tells a random joke."""
    url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            await update.message.reply_text(data["joke"])
    except (httpx.RequestError, KeyError) as e:
        logger.error(f"Error fetching joke: {e}")
        await update.message.reply_text("Sorry, I couldn't fetch a joke right now.")

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Rolls dice (e.g., /roll 2d6)."""
    args = context.args
    if not args or not re.match(r"^\d+d\d+$", args[0]):
        await update.message.reply_text("Please provide dice in NdS format (e.g., /roll 2d6).")
        return

    num_dice, num_sides = map(int, args[0].split("d"))
    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    await update.message.reply_text(f"You rolled: {', '.join(map(str, rolls))}. Total: {sum(rolls)}")

async def flip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Flips a coin."""
    result = random.choice(["Heads", "Tails"])
    await update.message.reply_text(f"It's {result}!")

async def rps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Play Rock, Paper, Scissors."""
    choices = ["rock", "paper", "scissors"]
    if not context.args or context.args[0].lower() not in choices:
        await update.message.reply_text("Please choose rock, paper, or scissors.")
        return

    user_choice = context.args[0].lower()
    bot_choice = random.choice(choices)

    result = ""
    if user_choice == bot_choice:
        result = "It's a tie!"
    elif (
        (user_choice == "rock" and bot_choice == "scissors")
        or (user_choice == "paper" and bot_choice == "rock")
        or (user_choice == "scissors" and bot_choice == "paper")
    ):
        result = f"You win! I chose {bot_choice}."
    else:
        result = f"You lose! I chose {bot_choice}."

    await update.message.reply_text(result)

async def eight_ball(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ask the magic 8-ball a question."""
    if not context.args:
        await update.message.reply_text("Please ask a question.")
        return

    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
    ]
    await update.message.reply_text(random.choice(responses))

async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a random picture of a cat."""
    url = "https://api.thecatapi.com/v1/images/search"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            await update.message.reply_photo(data[0]["url"])
    except (httpx.RequestError, KeyError) as e:
        logger.error(f"Error fetching cat picture: {e}")
        await update.message.reply_text("Sorry, I couldn't fetch a cat picture right now.")

async def dog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a random picture of a dog."""
    url = "https://dog.ceo/api/breeds/image/random"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            await update.message.reply_photo(data["message"])
    except (httpx.RequestError, KeyError) as e:
        logger.error(f"Error fetching dog picture: {e}")
        await update.message.reply_text("Sorry, I couldn't fetch a dog picture right now.")

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provides an inspirational quote."""
    url = "https://api.quotable.io/random"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            await update.message.reply_text(f'"{data["content"]}" - {data["author"]}')
    except (httpx.RequestError, KeyError) as e:
        logger.error(f"Error fetching quote: {e}")
        await update.message.reply_text("Sorry, I couldn't fetch a quote right now.")

async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get a random interesting fact."""
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            await update.message.reply_text(data["text"])
    except (httpx.RequestError, KeyError) as e:
        logger.error(f"Error fetching fact: {e}")
        await update.message.reply_text("Sorry, I couldn't fetch a fact right now.")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gets the current weather."""
    if not context.args:
        await update.message.reply_text("Please provide a city name.")
        return
    city = " ".join(context.args)
    # This requires an API key for a weather service.
    # For this example, we'll just return a placeholder.
    await update.message.reply_text(f"I can't get the weather for {city} yet, but I'm learning!")


async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gets the latest price of a cryptocurrency."""
    if not context.args:
        await update.message.reply_text("Please provide a cryptocurrency name (e.g., bitcoin).")
        return
    coin = context.args[0].lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            if coin in data and "usd" in data[coin]:
                price = data[coin]["usd"]
                await update.message.reply_text(f"The current price of {coin.capitalize()} is ${price:,.2f} USD.")
            else:
                await update.message.reply_text(f"Could not find the price for '{coin}'.")
    except httpx.RequestError as e:
        logger.error(f"Error fetching crypto price: {e}")
        await update.message.reply_text("Failed to fetch crypto price due to a network error.")


async def qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates a QR code."""
    if not context.args:
        await update.message.reply_text("Please provide text to encode in the QR code.")
        return
    text = " ".join(context.args)
    img = qrcode.make(text)
    bio = BytesIO()
    bio.name = 'qrcode.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    await update.message.reply_photo(photo=bio)


async def shorten(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shortens a long URL."""
    if not context.args:
        await update.message.reply_text("Please provide a URL to shorten.")
        return
    url = context.args[0]
    # This requires an API key for a URL shortening service.
    # For this example, we'll just return a placeholder.
    await update.message.reply_text(f"I can't shorten {url} yet, but I'm learning!")


async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Translates text to a specified language."""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /translate <lang_code> <text>")
        return
    lang = context.args[0]
    text = " ".join(context.args[1:])
    # This requires a translation API.
    # For this example, we'll just return a placeholder.
    await update.message.reply_text(f"I can't translate to {lang} yet, but I'm learning!")


async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """A simple calculator."""
    if not context.args:
        await update.message.reply_text("Please provide a mathematical expression.")
        return
    expression = "".join(context.args)
    try:
        # Sanitize expression to prevent security risks
        allowed_chars = "0123456789+-*/(). "
        if any(c not in allowed_chars for c in expression):
            raise ValueError("Invalid characters in expression")
        result = eval(expression)
        await update.message.reply_text(f"Result: {result}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Searches Wikipedia."""
    if not context.args:
        await update.message.reply_text("Please provide a search query.")
        return
    query = " ".join(context.args)
    try:
        page = wikipedia.page(query, auto_suggest=False)
        summary = page.summary.split('\n')[0]
        await update.message.reply_text(f"**{page.title}**\n{summary}...\n\n{page.url}")
    except wikipedia.exceptions.PageError:
        await update.message.reply_text(f"Sorry, I couldn't find a Wikipedia page for '{query}'.")
    except wikipedia.exceptions.DisambiguationError as e:
        options = "\n".join(e.options[:5])
        await update.message.reply_text(f"'{query}' is ambiguous. Did you mean one of these?\n{options}")


async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gets the current time in a city."""
    if not context.args:
        await update.message.reply_text("Please provide a city name.")
        return
    city = " ".join(context.args)
    # This requires a time zone API.
    # For this example, we'll just return a placeholder.
    await update.message.reply_text(f"I can't get the time for {city} yet, but I'm learning!")


async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Creates a poll in the chat."""
    if not context.args or len(context.args) < 3:
        await update.message.reply_text('Usage: /poll "Question" "Option 1" "Option 2" ...')
        return

    # The question and options are expected to be quoted strings
    args_str = " ".join(context.args)
    parts = [p.strip() for p in args_str.split('"') if p.strip()]

    if len(parts) < 3:
        await update.message.reply_text('Usage: /poll "Question" "Option 1" "Option 2" ...')
        return

    question = parts[0]
    options = parts[1:]

    await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=question,
        options=options,
        is_anonymous=False,
    )

async def define(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gets the definition of a word."""
    if not context.args:
        await update.message.reply_text("Please provide a word to define (e.g., /define hello).")
        return

    word = context.args[0]
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and data:
                definition = data[0]["meanings"][0]["definitions"][0]["definition"]
                await update.message.reply_text(f"**{word.capitalize()}**: {definition}")
            else:
                await update.message.reply_text(f"Could not find a definition for '{word}'.")
    except httpx.RequestError as e:
        logger.error(f"HTTP request failed: {e}")
        await update.message.reply_text("Failed to fetch definition due to a network error. Please try again later.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        await update.message.reply_text("An unexpected error occurred while fetching the definition. Please try again later.")

async def is_admin(update: Update, user_id: int) -> bool:
    """Checks if a user is an administrator in the chat."""
    chat_id = update.effective_chat.id
    try:
        chat_member = await update.effective_chat.get_member(user_id)
        return chat_member.status in ["administrator", "creator"]
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False

async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Pins the message it replies to (admins only)."""
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to pin it.")
        return

    if not await is_admin(update, update.effective_user.id):
        await update.message.reply_text("You must be an administrator to use this command.")
        return

    try:
        await update.message.reply_to_message.pin()
        await update.message.reply_text("Message pinned.")
    except Exception as e:
        logger.error(f"Error pinning message: {e}")
        await update.message.reply_text("Could not pin the message. Make sure I have pin permissions.")

async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unpins the current pinned message (admins only)."""
    if not await is_admin(update, update.effective_user.id):
        await update.message.reply_text("You must be an administrator to use this command.")
        return

    try:
        await update.effective_chat.unpin_all_messages()
        await update.message.reply_text("All messages unpinned.")
    except Exception as e:
        logger.error(f"Error unpinning messages: {e}")
        await update.message.reply_text("Could not unpin messages. Make sure I have unpin permissions.")

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Kicks a user from the group (admins only)."""
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to kick them.")
        return

    target_user = update.message.reply_to_message.from_user

    if not await is_admin(update, update.effective_user.id):
        await update.message.reply_text("You must be an administrator to use this command.")
        return

    if await is_admin(update, target_user.id):
        await update.message.reply_text("I cannot kick an administrator.")
        return

    try:
        await update.effective_chat.ban_member(target_user.id)
        await update.effective_chat.unban_member(target_user.id) # Unban immediately to allow rejoining
        await update.message.reply_text(f"User {target_user.mention_html()} kicked.")
    except Exception as e:
        logger.error(f"Error kicking user: {e}")
        await update.message.reply_text("Could not kick the user. Make sure I have kick permissions.")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bans a user from the group (admins only)."""
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to ban them.")
        return

    target_user = update.message.reply_to_message.from_user

    if not await is_admin(update, update.effective_user.id):
        await update.message.reply_text("You must be an administrator to use this command.")
        return

    if await is_admin(update, target_user.id):
        await update.message.reply_text("I cannot ban an administrator.")
        return

    try:
        await update.effective_chat.ban_member(target_user.id)
        await update.message.reply_text(f"User {target_user.mention_html()} banned.")
    except Exception as e:
        logger.error(f"Error banning user: {e}")
        await update.message.reply_text("Could not ban the user. Make sure I have ban permissions.")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mutes a user for a specified time (admins only)."""
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to mute them.")
        return

    target_user = update.message.reply_to_message.from_user

    if not await is_admin(update, update.effective_user.id):
        await update.message.reply_text("You must be an administrator to use this command.")
        return

    if await is_admin(update, target_user.id):
        await update.message.reply_text("I cannot mute an administrator.")
        return

    try:
        # Mute for 1 hour
        until_date = datetime.now() + timedelta(hours=1)
        permissions = ChatPermissions(can_send_messages=False)
        await update.effective_chat.restrict_member(target_user.id, permissions, until_date=until_date)
        await update.message.reply_text(f"User {target_user.mention_html()} muted for 1 hour.")
    except Exception as e:
        logger.error(f"Error muting user: {e}")
        await update.message.reply_text("Could not mute the user. Make sure I have restrict permissions.")