![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Telegram](https://img.shields.io/badge/Telegram-3670A0?style=for-the-badge&logo=telegram&logoColor=white)


# Бот "Игра глаголов"

Бот-помощник, «Игра глаголов» – крупное онлайн-издательство, помогающее продвигать авторские блоги и публиковать книги. 

## Установка.
- Python3 (версия Python 3.10) должен быть уже установлен.
- Рекомендуется использовать среду окружения [venv](https://docs.python.org/3/library/venv.html) 
для изоляции проекта.
 - Используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей
```console
$ pip install -r requirements.txt
```


### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

- `TG_BOT_TOKEN=HERE_TOKEN_TELEGRAM_BOT` - Токен ключ телеграм бота
- `DIALOGFLOW_PROJECT_ID=HERE_PROJECT_ID` - Проект ID DialogFlow
- `GOOGLE_APPLICATION_CREDENTIALS` - имя файла json authenticate by using API keys
- `VK_COMMUNITY_TOKEN` - токен группы в контакте


## Запуск

```console
$ python3 game_verbs_bot.py
```
```console
$ python3 game_verbs_bot_vk.py
```
## Скрипт обучения на DialogFlow
```console
$ python3 intent_management.py file_name
```

`file_name` Имя json файла с вопросами и ответом для создания Intent на DialogFlow.

## Работающие боты
[VK](https://vk.com/public223195342) и [Telegram](https://t.me/pvg_game_of_verbs_bot)

## Пример работы бота
![](https://github.com/vladpap/game_verbs_bot/blob/main/game_of_verbs_bot.gif)

## Цели проекта

Код написан в учебных целях — это командный проект на курсе по Python [Devman](https://dvmn.org).


<img src="https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg" alt= “” width="102" height="25">