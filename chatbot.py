from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, 
                          CallbackContext)
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT
# import re

global redis1
def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']))
   
    # You can set this logging module, so you will know when and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    # chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    message_handler = MessageHandler(Filters.text & (~Filters.command), keywords)
    dispatcher.add_handler(message_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    # dispatcher.add_handler(CommandHandler("help", help_command))
    # dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(CommandHandler("test", status_check))
    dispatcher.add_handler(CommandHandler("query", query))
    dispatcher.add_handler(CommandHandler("GptON", openGpt))
    dispatcher.add_handler(CommandHandler("GptOFF", closeGpt))
    
    # To start the bot:
    updater.start_polling()
    updater.idle()

GPTFlag = False

def openGpt(update, context):
    GPTFlag = True
    equiped_chatgpt(update,context,'if you receive this message, please answer me "Hello, Im the GPT assistant. Im ready to help you coding."')
    return

def closeGpt(update, context):
    GPTFlag = False
    return

# def echo(update, context):
#     reply_message = update.message.text.upper()
#     logging.info("Update: " + str(update))
#     logging.info("context: " + str(context))
#     context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

def query(update: Update, context: CallbackContext) -> None:
    mesString = context.args[0].lower()+context.args[1].lower()
    
    if(len(context.args)>=3):
        # Implementation = "$.." + context.args[2].lower() + "Implementation"
        list = []
        for index, msg in enumerate(context.args):
        # msgQ = context.args[0].lower().replace(" ","")
            if(msg.lower() == 'description'):
                list.append("$.." + 'Description')
                continue
            if(msg.lower() == 'time' or msg.lower() == 'complexity'):
                list.append("$.." + 'TimeComplexity')
                continue
            if(msg.lower() == 'application'or msg.lower() == 'scenarios'):
                list.append("$.." + 'ApplicationScenarios')
                continue
            else:
                if(index>1):
                    list.append("$.." + msg.lower() + "Implementation")
        # msgQ = mesString
        print(mesString)
        print(list)
        for q in list:
            try:
                # reply = redis1.get('testJson').decode('UTF-8')
                reply = redis1.json().get(mesString, q)
                reply = reply[0]
                print(reply)
                update.message.reply_text(reply)
            except (IndexError, ValueError):
                update.message.reply_text('Sorry, error in redis connection.')
    else:
        # for msg in context.args:
        #     mesString += msg.lower()
        # msgQ = context.args[0].lower().replace(" ","")
        # msgQ = mesString
        # print(msgQ)
        try:
            # reply = redis1.get('testJson').decode('UTF-8')
            reply = redis1.json().get(mesString, "$")
            reply = reply[0]['Description']
            # print(reply)
            update.message.reply_text(reply)
        except (IndexError, ValueError):
            update.message.reply_text('Sorry, error in redis connection.')
    

def equiped_chatgpt(update, context, mes): 
    global chatgpt
    reply_message = chatgpt.submit(mes)
    logging.info("GPTUpdate: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# def help_command(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Helping you helping you.')

def status_check(update: Update, context: CallbackContext)-> None:
    update.message.reply_text('status check')
    # try:
    #     msg = 'testMsg'
    #     reply = redis1.get(msg).decode('UTF-8')
    #     print(reply)
    #     update.message.reply_text(reply)
    # except (IndexError, ValueError):
    #     update.message.reply_text('Sorry, error in redis connection.')

def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

# def hello_command(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /hello is issued."""
#     msg = context.args[0]
#     update.message.reply_text('Good day, \n'+ msg +'!')

def keywords(update: Update, context: CallbackContext):
    update.message.reply_text('You just say the keywords!')
    print(update.message.text)
    msg = update.message.text.lower()
    resultJs = msg.find(' javascript ')
    resultJ = msg.find(' java ')
    resultPy = msg.find(' python ')
    resultC = msg.find(' C ')
    resultCPP = msg.find(' C++ ')
    resultCS = msg.find(' C# ')
    resultCSS = msg.find(' CSS ')
    resultHTML = msg.find(' html ')

    keys = ['javascript','java','python','C','C++','C#','CSS','html']
    values = [resultJs,resultJ,resultPy,resultC,resultCPP,resultCS,resultCSS,resultHTML]

    results = dict(zip(keys,values))

    for key ,value in results.items():
        if (value > -1):
            print(key)
            try:
                redis1.incr(msg)
                print('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
            except (IndexError, ValueError):
                update.message.reply_text('Sorry, error in redis connection.')

    if GPTFlag:
        equiped_chatgpt(update,context,)


if __name__ == '__main__':
    main()
