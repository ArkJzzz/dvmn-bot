# dvmn-bot 

Telegram-бот для уведомлений о проверке работ на [Devman](https://dvmn.org) - онлайн-курсе по программированию на Python.


## Что используется

- [python-telegram-bot](https://python-telegram-bot.org/)
- [API Devman](https://dvmn.org/api/docs/)
- Long Polling


## Требования к окружению

1. Получить токен для дуступа к [API Devman](https://dvmn.org/api/docs/)
2. Зарегистрировать бота в Telegram:

    - написать [Отцу ботов](https://telegram.me/BotFather):

        ```
        \start
        ```

        ```
        \newbot
        ```
    
    - получить токен для доступа к API Telegram


## Установка

Клонировать репозиторий:

```bash
git clone https://github.com/ArkJzzz/dvmn-bot.git
```

Создать файл ```.env``` и поместить в него токены Devman и Telegram:

```
TELEGRAM_TOKEN='Ваш токен'
DVMN_TOKEN='Ваш токен'
```

Установить зависимости: 

```bash
pip3 install -r requirements.txt
```

## Запуск

```bash
python3 main.py
```


