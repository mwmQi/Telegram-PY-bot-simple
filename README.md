# 🤖 Feature-Rich Telegram Bot

This is a powerful and versatile Telegram bot built with the `python-telegram-bot` library. It offers a wide range of features, from fun and games to utility tools and group administration. The bot is designed to be easily extensible, allowing you to add new commands and features with minimal effort.

## ✨ Features

###  बेसिक Commands

- `/start`: Welcomes the user and provides a brief introduction to the bot.
- `/help`: Lists all available commands with a short description of each.
- `/ping`: Checks if the bot is responsive and provides a "Pong!" message.
- `/uptime`: Shows how long the bot has been running since its last restart.
- `/info`: Gets detailed information about the user or chat, including user ID, name, and chat type.

### 🎮 Fun & Games

- `/joke`: Tells a random joke from a collection of jokes.
- `/roll <NdS>`: Rolls dice in the format of NdS (e.g., `/roll 2d6` for two 6-sided dice).
- `/flip`: Flips a coin and returns either "Heads" or "Tails."
- `/rps <rock|paper|scissors>`: Lets you play a game of Rock, Paper, Scissors against the bot.
- `/8ball <question>`: Ask the magic 8-ball a question and get a mysterious answer.
- `/cat`: Sends a random picture of a cat from the internet.
- `/dog`: Sends a random picture of a dog from the internet.
- `/quote`: Provides an inspirational quote to brighten your day.
- `/fact`: Get a random interesting fact from a curated list.

### 🛠️ Utility Tools

- `/weather <city>`: Gets the current weather for a specified city.
- `/crypto <coin>`: Gets the latest price of a cryptocurrency (e.g., Bitcoin, Ethereum).
- `/qr <text>`: Generates a QR code for the given text.
- `/shorten <url>`: Shortens a long URL to a more manageable length.
- `/translate <lang> <text>`: Translates text to a specified language using an online translation service.
- `/calc <expression>`: A simple calculator that can evaluate mathematical expressions.
- `/wiki <query>`: Searches Wikipedia for a given query and returns a summary of the article.
- `/time <city>`: Gets the current time in a specified city.
- `/poll`: Creates a poll in the chat with a question and multiple options.
- `/define <word>`: Gets the definition of a word from an online dictionary.

### 👑 Group Admin

- `/pin`: Pins the message it replies to (admins only).
- `/unpin`: Unpins the current pinned message (admins only).
- `/kick @user`: Kicks a user from the group (admins only).
- `/ban @user`: Bans a user from the group (admins only).
- `/mute @user`: Mutes a user for a specified time (admins only).

## 🚀 Getting Started

To get started with the bot, you will need to have Python 3.12+ and pip installed on your system. You will also need a Telegram bot token, which you can get from the BotFather.

### 1. Set up the project

Once you have the project files, it is recommended to create a virtual environment to manage the project's dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

Next, install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### 2. Get Your Bot Token

1.  Open Telegram and search for `@BotFather`.
2.  Start a chat with BotFather and send `/newbot`.
3.  Follow the instructions to choose a name and username for your bot.
4.  BotFather will provide you with an API token (a long string of letters and numbers).

### 3. Configure the Bot Token

The bot token can be provided in two ways:

1.  **Environment Variable (Recommended):** Set the `TELEGRAM_BOT_TOKEN` environment variable before running the bot.
    ```bash
    export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
    ```
   
    Replace `"YOUR_BOT_TOKEN"` with the actual token you received from BotFather.

2.  **Interactive Prompt:** If the `TELEGRAM_BOT_TOKEN` environment variable is not set, the bot will prompt you to enter the token when you run `main.py`.

### 4. Run the Bot

Once you have installed the dependencies and configured the bot token, you can run the bot by executing the following command:

```bash
python main.py
```

The bot should now be running and accessible in your Telegram account.

## 📁 Project Structure

```
telegram_bot/
├── venv/
├── main.py
├── handlers.py
├── utils.py
└── requirements.txt
```

-   `venv/`: This directory contains the Python virtual environment for the project. It isolates the project's dependencies from the global Python installation, ensuring that the bot runs in a consistent and predictable environment. The `venv` directory is created when you run `python3 -m venv venv` and is activated with `source venv/bin/activate`.
-   `main.py`: The main entry point of the bot, responsible for setting up the application and registering command handlers.
-   `handlers.py`: Contains all the asynchronous functions that handle specific Telegram commands (e.g., `/start`, `/help`, `/joke`).
-   `utils.py`: Contains utility functions and variables used across different parts of the bot, such as logging configuration and `start_time` for uptime calculation.
-   `requirements.txt`: Lists all the Python dependencies required to run the bot.

## 📦 Dependencies

The bot relies on the following Python libraries:

- `python-telegram-bot`: The main library used to interact with the Telegram Bot API.
- `httpx`: A modern and asynchronous HTTP client used for making API requests.
- `wikipedia`: A Python library that makes it easy to access and parse data from Wikipedia.
- `qrcode`: A library for generating QR codes.

All the required dependencies are listed in the `requirements.txt` file and can be installed by running `pip install -r requirements.txt`.
