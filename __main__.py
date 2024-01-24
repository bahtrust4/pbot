import asyncio

# from fastapi import FastAPI
from telebot import ExceptionHandler
from telebot.types import Message
from telebot.asyncio_storage import StateMemoryStorage

from telebot_nav import TeleBotNav
from config import TELEGRAM_TOKEN
from config import ALLOWED_USER_NAMES
# from config import NGROK_TUNNEL_URL

import config
import replicaMod
import youtube_dl_module
from logger import logger

from openaiMod import ChatGpTRouter, TTSRouter

# app = FastAPI()
# # WEBHOOK_PATH = f"/bot/{TELEGRAM_TOKEN}"
# # WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"

# async def make_request_to_server(endpoint: str, data: dict = None):
#     async with app.client.session() as session:
#         async with session.post(f"http://ваш-адрес-сервера/{endpoint}", json=data) as response:
#             print(endpoint)
#             response_data = await response.json()
#             return response_data
                

class ExceptionH(ExceptionHandler): 
    def handle(self, exception: Exception):   
        logger.exception(exception)

async def start(botnav: TeleBotNav, message: Message) -> None:
    logger.info(f'{message.from_user.username} {message.chat.id}')
    username = botnav.get_user(message).username   

    if (ALLOWED_USER_NAMES and (
            not username or
            username.lower() not in ALLOWED_USER_NAMES
        )
    ):
        logger.info(f'{username} {message.chat.id} незваный гость')
        await botnav.bot.send_message(message.chat.id, "not work")
        return
    
    #server_response = await make_request_to_server("some-endpoint", data={"user_id": message.chat.id})
    #print(server_response)

    await botnav.print_buttons(
        message.chat.id,
        {
            '📷 Replicate': replicaMod.start_replicate if config.REPLICATE_API_KEY else None,
            # '👽 OpenAI': openaiMod.start_openai if config.OPENAI_API_KEY else None,
            '👁 Ютуб URL': youtube_dl_module.start_youtube_dl,
            '🤖 Chat GPT': ChatGpTRouter.run,
            '👽 GPT опции': ChatGpTRouter.show_chat_options,
            '🗣 TTS | Изменение Голоса': TTSRouter.run,
        }, f'▫️ Приветствуем вас, {message.from_user.first_name}.\n \nДля начала работы запустите свои мыслительные процессы и выберите инструмент:',
        row_width=2
    )

    botnav.wipe_commands(message)
    botnav.add_command(message, 'start', '👁 Запуск', start)
    await botnav.send_commands(message)


async def main() -> None:
    await botnav.send_init_commands({'start': '👁 Запуск'})
    await botnav.set_global_default_handler(start)
    await botnav.bot.polling()


botnav = TeleBotNav(
    TELEGRAM_TOKEN,
    state_storage=StateMemoryStorage(),
    exception_handler=ExceptionH()
)


if __name__ == '__main__':
    asyncio.run(main())

# if __name__ == "__main__":
#     import uvicorn  # для сервера ASGI
# uvicorn.run(app, host="localhost", port=8000)  