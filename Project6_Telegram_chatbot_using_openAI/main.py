from dotenv import load_dotenv
import os
# import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import sys

load_dotenv()
OPENAI_API_KEY =os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

class Reference:
    '''
    A class to store previously response from the openai API
    '''

    def __init__(self) -> None:
        self.response = ""

reference = Reference()
model_name = "gpt-3.5-turbo"

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""

# Define command handler for /start 
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi\nI am Bot! Created by Reek. \n How are you doing today?")

# Define command handler for /clear 
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_past()
    await update.message.reply_text("I've cleared the past conversation and context.")

# Define command handler for  /help
async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm Telegram bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await update.message.reply_text(help_command)
    
async def chatgpt(update:Update,context:ContextTypes.DEFAULT_TYPE):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{update.message.text}")
    response = openai.chat.completions.create(
        model=model_name,
        messages= [
            {"role":"assistant","content":reference.response}, #role assitant
            {"role":"user","content":update.message.text}
        ]
    )
    reference.response = response.choices[0].message.content
    print(f">>> chatGPT: \n\t{reference.response}")
    await update.message.reply_text(reference.response)



if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler(["start"], welcome))
    app.add_handler(CommandHandler(["help"], helper))
    app.add_handler(CommandHandler(["clear"], clear))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt))

    # Run the bot 
    app.run_polling() 
    # drop_pending_updates=False is by default which means all the message sent when the backend is offline
    # will be sent when reconnected