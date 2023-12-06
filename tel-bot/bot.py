from sys import argv
from time import sleep

from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener
from origamibot.core.teletypes.message import Message

import requests
import freecurrencyapi
from datetime import datetime

SEARCH_URI = "https://www.google.com/search?q="

class Logger:
    def __init__(self) -> None:
        self.log_file = open("bot_log.log", mode="a")

    def write(self, text: str):
        self.log_file.write(f"{datetime.now()} {text.strip()}\n")
        self.log_file.flush()

logger = Logger()


class BotsCommands:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.cclient = freecurrencyapi.Client("fca_live_G3DdF4IEQVFyQPH1UqBYO0BJ0PMW2RB4jrkdiBzR")

    def search(self, message: Message, *args):
        text = '+'.join(args)
        self.bot.send_message(
            message.chat.id, 
            SEARCH_URI+text
        )
        print(f"[{message.chat.id}, {message.chat.username}]:[SENT] {SEARCH_URI+text}")
        logger.write(f"[{message.chat.id}, {message.chat.username}]:[SENT] {SEARCH_URI+text}")

    def weather(self, message: Message, city: str):
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key=263480053f73422fa5893539230412&q={city}&aqi=no")
        if response.status_code == 400:
            self.bot.send_message(
                message.chat.id,
                "400 | Error. Might no matching location found."
            )
            print(f"[USER FAIL][{message.chat.id}, {message.chat.username}]:[SENT] 400 | Error. Might no matching location found.")
            logger.write(f"[USER FAIL][{message.chat.id}, {message.chat.username}]:[SENT] 400 | Error. Might no matching location found.")
            return
        
        temp_c = response.json()['current']['temp_c']
        self.bot.send_message(
            message.chat.id,
            str(temp_c)
        )

        print(f"[{message.chat.id}, {message.chat.username}]:[SENT] {temp_c}")
        logger.write(f"[{message.chat.id}, {message.chat.username}]:[SENT] {temp_c}")

    def currency(self, message, fromc: str, toc: str):
        cresult = None
        try:
            cresult = self.cclient.latest(base_currency=fromc, currencies=[toc])
        except:
            self.bot.send_message(
                message.chat.id,
                "400 | Error. Might not valid currencies"
            )
            print(f"[USER FAIL][{message.chat.id}, {message.chat.username}]:[SENT] 400 | Error. Might not valid currencies")
            logger.write(f"[USER FAIL][{message.chat.id}, {message.chat.username}]:[SENT] 400 | Error. Might not valid currencies")
            return
        
        currency = cresult['data'][toc]
        self.bot.send_message(
            message.chat.id,
            f"{fromc}: {currency} {toc}"
        )
        print(f"[{message.chat.id}, {message.chat.username}]:[SENT] {fromc}: {currency} {toc}")
        logger.write(f"[{message.chat.id}, {message.chat.username}]:[SENT] {fromc}: {currency} {toc}")

    # def schedule(self, message, type: str, time: int):
    #     if type != 'currency' or type != 'weather':
    #         self.bot.send_message(
    #             message.chat.id,
    #             '? | No matching type'
    #         )
    #         print(f"[USER FAIL][{message.chat.id}, {message.chat.username}]:[SENT] ? | No matching type")
    #         logger.write(f"[USER FAIL][{message.chat.id}, {message.chat.username}]:[SENT] ? | No matching type")
    #         return
        
    #     if type == 'currency':
    #         pass
    #     elif type == 'weather':
    #         pass


class MessageListener(Listener): 
    def __init__(self, bot):
        self.bot = bot

    def on_message(self, message: Message):
        print(f"[{message.chat.id}, {message.chat.username}]: {message.text}")
        logger.write(f"[{message.chat.id}, {message.chat.username}]: {message.text}")

    def on_command_failure(self, message, err=None):
        if err is None:
            self.bot.send_message(message.chat.id,
                                  'Command failed to bind arguments!')
            print(f"[USER FAIL][{message.chat.id}, {message.chat.username}]:[SENT] Command failed to bind arguments!")
            logger.write(f"[USER FAIL][{message.chat.id}, {message.chat.username}]: Command failed to bind arguments!")
        else:
            self.bot.send_message(message.chat.id,
                                  f'Error')
            print(f"[ERROR][{message.chat.id}, {message.chat.username}]:[SENT] Error")
            logger.write(f"[ERROR][{message.chat.id}, {message.chat.username}]:[SENT] Error")

if __name__ == '__main__':
    token = '5511513570:AAGnBWyRqebgkfbGiTTcdZEtUwEBI1QBhFc'
    # token = (argv[1] if len(argv) > 1 else input('Enter bot token: '))
    bot = Bot(token)

    bot.add_listener(MessageListener(bot))
    bot.add_commands(BotsCommands(bot))

    bot.start() 
    while True:
        sleep(1)