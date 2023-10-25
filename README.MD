![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Telegram](https://img.shields.io/badge/Telegram-3670A0?style=for-the-badge&logo=telegram&logoColor=white)

# Бот "Игра глаголов"

Бот-помощник, «Игра глаголов» – крупное онлайн-издательство, помогающее продвигать авторские блоги и публиковать книги. 

## Установка.
- Python3 (версия Python 3.11.3) должен быть уже установлен.
- Рекомендуется использовать среду окружения [venv](https://docs.python.org/3/library/venv.html) 
для изоляции проекта.
 - Используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей
```console
$ pip install -r requirements.txt
```

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

- `TG_BOT_TOKEN=HERE_TOKEN_TELEGRAM_BOT` - Токен ключ телеграм бота

## Запуск

```console
$ python3 game_verbs_bot.py
```

## Цели проекта

Код написан в учебных целях — это командный проект на курсе по Python [Devman](https://dvmn.org).


<img src="https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg" alt= “” width="102" height="25">