import os
from uuid import uuid4
from app import data

from telegram import InlineQueryResultVoice, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultVoice(
            id=uuid4(),
            title=audio['title'],
            voice_url=audio['src'],
        )
        for audio in data.search_entries(title__search=query)
    ]

    update.inline_query.answer(results)


def start_bot() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = os.environ['BOT_TOKEN']

    PORT = int(os.environ.get('PORT', '8443'))

    updater = Updater(TOKEN, use_context=True)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://dotasound.herokuapp.com/" + TOKEN)

    updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
