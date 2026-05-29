import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from anthropic import Anthropic

from memory import save_message, load_memory
from knowledge import search_knowledge

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=ANTHROPIC_API_KEY)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


def get_knowledge_context(query):
    try:
        results = search_knowledge(query)

        if not results:
            return ""

        context = ""

        for result in results[:3]:
            context += result["content"]
            context += "\n\n"

        return context[:12000]

    except Exception:
        return ""


@dp.message()
async def handle_message(message: Message):
    user_text = message.text

    if not user_text:
        return

    user_id = str(message.from_user.id)

    history = load_memory(user_id)

    knowledge_context = get_knowledge_context(user_text)

    await bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    try:
        messages = history.copy()

        if knowledge_context:
            messages.append({
                "role": "user",
                "content": knowledge_context
            })

        messages.append({
            "role": "user",
            "content": user_text
        })

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=messages
        )

        reply = response.content[0].text

        save_message(user_id, "user", user_text)
        save_message(user_id, "assistant", reply)

        await message.answer(reply)

    except Exception as e:
        await message.answer(f"Error: {str(e)}")


async def main():
    print("Bot running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
