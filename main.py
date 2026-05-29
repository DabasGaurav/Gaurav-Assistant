import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from anthropic import Anthropic

# Load keys from .env
load_dotenv()

# Get keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Claude client
client = Anthropic(
    api_key=ANTHROPIC_API_KEY
)

# Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Handle incoming messages
@dp.message()
async def handle_message(message: Message):

    user_text = message.text

    # show "typing..."
    await bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    try:

        # Ask Claude
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        # Extract Claude reply
        reply = response.content[0].text

        # Send reply back
        await message.answer(reply)

    except Exception as e:
        await message.answer(f"Error: {str(e)}")

# Start bot
async def main():
    print("Bot running...")
    await dp.start_polling(bot)

# Run app
if __name__ == "__main__":
    asyncio.run(main())