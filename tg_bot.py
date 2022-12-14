import logging

from environs import Env
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext
)

from dialogflow import get_reply_by_intent

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Здравствуйте!')


def reply(update: Update, context: CallbackContext):
    _, fulfillment_text = get_reply_by_intent(
        context.bot_data.get('project_id'),
        update.message.chat_id,
        update.message.text,
        context.bot_data.get('language_code')
    )
    update.message.reply_text(
        text=fulfillment_text
    )


def main():
    env = Env()
    env.read_env()
    bot_token = env('TELEGRAM_BOT_TOKEN')
    project_id = env('PROJECT_ID')
    language_code = env('LANGUAGE_CODE')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)

    updater = Updater(bot_token)

    dispatcher = updater.dispatcher
    dispatcher.bot_data.update(
        {
            'project_id': project_id,
            'language_code': language_code,
        }
    )
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, reply)
    )

    logger.info('Telegram bot is running.')

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
