import logging

from environs import Env
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from my_detect_intent import detect_intent_text

logger = logging.getLogger('game verbs telegram bot')


def start(update: Update, context: CallbackContext) -> None:

    update.message.reply_text('Здравствуйте')


def get_response_from_dialogflow(update: Update, context: CallbackContext) -> None:
    message_to_dialogflow = update.message.text
    session_id = update.effective_chat.id
    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    try:
        serialized_answer = detect_intent_text(
            project_id,
            session_id,
            message_to_dialogflow)
        update.message.reply_text(serialized_answer['fulfillment_text'])

    except response.exceptions.ConnectionError:
        logger.exception('Problem connection.')

    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    logger.info('Start telegram bot')

    tg_token = env.str('TG_BOT_TOKEN')

    updater = Updater(tg_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, get_response_from_dialogflow))

    updater.start_polling()

    updater.idle()
