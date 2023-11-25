import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage,SystemMessage



Token = getenv('TOKEN')
openai.api_key = getenv('OPENAI_API_KEY')

bot = Bot(Token, parse_mode=ParseMode.HTML)
dp = Dispatcher()

chat = ChatOpenAI(max_tokens=520,temperature=0.5)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.reply(f"Hello, {hbold(message.from_user.full_name)}! \n I am Chat Bot Project, Made by {hbold('Ahmed')} \n How can i help you ? ")



@dp.message(Command(commands=['help']))
async def helper(message:Message):
    to_send = f'''
    Hello {hbold(message.from_user.first_name)} ! 
Follow these Commands: 
    /start : To Start the Coversation 
    /clear : To Clear all Conversation 
    /help : To view the Help menu 
    
{hbold("You can ask me anything, except the naughty stuff ;)")}'''
    await message.answer(to_send)



@dp.message()
async def convo(message:Message):
    query = message.text

    message_for_ai = [ 
        SystemMessage(content= 'You are a General purpose Chat bot'),
        HumanMessage(content=query)
    ]

    to_send = chat(message_for_ai)
    to_send = to_send.content
    print(f"By User : {query} /n By AI {to_send}")
    await message.answer(to_send)

async def main() -> None:
    await dp.start_polling(bot,skip_updates = False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())