import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, CallbackContext

from environs import Env

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:

    update.message.reply_text('Здравствуйте')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    env = Env()
    env.read_env()

    TG_TOKEN = env.str('TG_BOT_TOKEN')

    updater = Updater(TG_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
