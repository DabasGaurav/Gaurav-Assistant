import asyncio
import os

from memory import save_message, load_memory
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from anthropic import Anthropic
from knowledge import search_knowledge

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

    if user_text.startswith("/search"):
        query = user_text.replace("/search", "").strip()

        results = search_knowledge(query)

        if len(results) == 0:
            await message.answer("No results found.")
            return

        response_text = ""

        for result in results[:3]:
            response_text += f"\nFILE: {result['file']}\n\n"
            response_text += result["content"]
            response_text += "\n\n-------------------\n\n"

        await message.answer(response_text[:4000])
        return


    user_id = str(message.from_user.id)
    history = load_memory(user_id)

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
            messages=history + [
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        # Extract Claude reply
        reply = response.content[0].text
        save_message(user_id, "user", user_text)
        save_message(user_id, "assistant", reply)

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