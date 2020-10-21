#!usr/bin/python3.7

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'

import requests
import os
import sys
import argparse
import telegram
import logging
from logging.handlers import RotatingFileHandler
# from dotenv import load_dotenv


def check_dvmn_tasks(url, headers, payload, timeout):
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=timeout, params=payload)
            response.raise_for_status()
            answer = response.json()
            status = answer['status']
            if status == 'found':
                new_attempts = answer['new_attempts']
                for new_attempt in new_attempts:
                    timestamp = new_attempt['timestamp']
                    return new_attempt
            elif status == 'timeout':
                timestamp = answer['timestamp_to_request']
                raise requests.exceptions.ReadTimeout
            else:
                raise requests.exceptions.HTTPError
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            pass


def extract_dvmn_check_result(new_attempt):
    if new_attempt['is_negative']:
        feedback = 'Преподаватель рекомендует доработать решение.'
    else:
        feedback = 'Преподавателю все понравилось, можно приступать к следующему уроку!'

    dvmn_check_result = 'Преподаватель проверил работу: {lesson_title}. \n\n{feedback}'.format(
        lesson_title=new_attempt['lesson_title'],
        feedback=feedback
        )

    return dvmn_check_result


def send_telegram_message(bot, chat_id, message_to_send):
    updates = bot.get_updates()
    chat_id=chat_id

    bot.send_message(
        chat_id=chat_id, 
        text='Привет!  \n\n{message_to_send}'.format(
            message_to_send=message_to_send
            )
        )


class MyLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: \n\n%(message)s')
        self.setFormatter(formatter)
        self.bot = bot
        self.chat_id = chat_id
    
    def emit(self, record):      
        log_entry = self.format(record)
        send_telegram_message(self.bot, self.chat_id, log_entry)


def main():

    # init

    # load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    devman_token = os.environ['DVMN_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    bot = telegram.Bot(token=telegram_token)
    bot.deleteWebhook()
    
    url = 'https://dvmn.org/api/long_polling'
    headers = {'Authorization': devman_token}
    timestamp = None
    payload = {'timestamp':timestamp}
    timeout = 60

    logger = logging.getLogger('BotLogger')    
    logger.setLevel(logging.DEBUG)
    handler = MyLogsHandler(bot, chat_id)
    logger.addHandler(handler)
    
    logger.info('Бот запущен')

    # do

    while True:
        try:
            new_attempt = check_dvmn_tasks(url, headers, payload, timeout)
            message_to_send = extract_dvmn_check_result(new_attempt)
            send_telegram_message(bot, chat_id, message_to_send)
        except KeyboardInterrupt:
            logger.info('Бот остановлен')
        except Exception  as err:
            logger.error('Бот упал с ошибкой:')
            logger.error(err)
            logger.debug(err, exc_info=True)


if __name__ == "__main__":
    main()
