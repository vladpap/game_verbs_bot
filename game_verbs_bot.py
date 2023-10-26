import logging

from environs import Env
from google.cloud import api_keys_v2, dialogflow
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def create_api_key(project_id):
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = "My first API key"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()
    return response


def start(update: Update, context: CallbackContext) -> None:

    update.message.reply_text('Здравствуйте')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


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

    DF_TOKEN = create_api_key(project_id)
    print("Successfully created an API key")

    TG_TOKEN = env.str('TG_BOT_TOKEN')
    updater = Updater(TG_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo_dialogflow))

    updater.start_polling()

    updater.idle()
