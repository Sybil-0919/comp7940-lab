'''
This program requires the following modules:
- python-telegram-bot==22.5
- urllib3==2.6.2
- requests
'''
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from ChatGPT_HKBU import ChatGPT
import configparser
import logging

# Global variable for ChatGPT client
gpt = None


def main():
    global gpt

    # Configure logging so you can see initialization and error messages
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Load the configuration data from file
    logging.info('INIT: Loading configuration...')
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Create a ChatGPT client object
    gpt = ChatGPT(config)

    # Create an Application for your bot
    logging.info('INIT: Connecting the Telegram bot...')
    app = ApplicationBuilder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()

    # Register a message handler
    logging.info('INIT: Registering the message handler...')
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, callback))

    # Start the bot
    logging.info('INIT: Initialization done!')
    app.run_polling()


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("UPDATE: " + str(update))

    # Show a "Thinking..." message while waiting for ChatGPT
    loading_message = await update.message.reply_text('Thinking...')

    # Send the user message to the ChatGPT client
    response = gpt.submit(update.message.text)

    # Send the response to the Telegram bot client
    await loading_message.edit_text(response)


if __name__ == '__main__':
    main()