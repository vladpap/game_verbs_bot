import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:

    update.message.reply_text('Здравствуйте')


def detect_intent_text(project_id,
                       session_id,
                       message_to_dialogflow,
                       language_code='ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=message_to_dialogflow,
        language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    serialized_answer = {
        'intention': response.query_result.intent.display_name,
        'confidence': response.query_result.intent_detection_confidence,
        'answer': response.query_result.fulfillment_text
    }
    return serialized_answer


def echo_dialogflow(update: Update, context: CallbackContext) -> None:
    message_to_dialogflow = update.message.text
    session_id = update.effective_chat.id
    serialized_answer = detect_intent_text(
        project_id,
        session_id,
        message_to_dialogflow)
    update.message.reply_text(serialized_answer['answer'])


if __name__ == '__main__':
    env = Env()
    env.read_env()

    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    TG_TOKEN = env.str('TG_BOT_TOKEN')

    updater = Updater(TG_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo_dialogflow))

    updater.start_polling()

    updater.idle()
