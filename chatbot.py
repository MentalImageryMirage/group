from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, 
                          CallbackContext)
import configparser
import logging
# import redis
from mongoDB import mongoDBconnect
from ChatGPT_HKBU import HKBU_ChatGPT
# import re
import os

# global redis1
global mongoDB
global GPTFlag
def main():
    # Load your token and create an Updater for your Bot
    global GPTFlag
    GPTFlag = False
#    config = configparser.ConfigParser()
#    config.read('config.ini')
#    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    # global redis1
    # redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']))
    global mongoDB
    mongoDB = mongoDBconnect()
    # You can set this logging module, so you will know when and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # dispatcher for chatgpt
    global chatgpt
#    chatgpt = HKBU_ChatGPT(config)
    chatgpt = HKBU_ChatGPT()
    # chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    message_handler = MessageHandler(Filters.text & (~Filters.command), keywords)
    dispatcher.add_handler(message_handler)

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("add", add))
    # dispatcher.add_handler(CommandHandler("help", help_command))
    # dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("test", status_check))
    dispatcher.add_handler(CommandHandler("query", query))
    dispatcher.add_handler(CommandHandler("GptON", openGpt))
    dispatcher.add_handler(CommandHandler("GptOFF", closeGpt))
    dispatcher.add_handler(CommandHandler("statistic", showStatistic))
    
    # To start the bot:
    updater.start_polling()
    updater.idle()

def start(update, context):
    update.message.reply_text("Welcome.I'm your coding assistant.\nThere are a number of commands you can use to access my features to assist you in writing code. Also I count keywords in the chat logs about computer programming languages.\nTry commands:\n/query\n/GptON\n/GptOFF\n/statistic")

def openGpt(update, context):
    global GPTFlag
    GPTFlag = True
    update.message.reply_text("GPT ON, please wait.")
    equiped_chatgpt(update,context,'if you receive this message, please answer me "Hello, Im the GPT assistant. Im ready to help you coding."')
    return

def closeGpt(update, context):
    update.message.reply_text("GPT off.")
    global GPTFlag
    GPTFlag = False
    return

# def echo(update, context):
#     reply_message = update.message.text.upper()
#     logging.info("Update: " + str(update))
#     logging.info("context: " + str(context))
#     context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

def query(update: Update, context: CallbackContext) -> None:
    if(len(context.args)==0):
        replyMsg = "This function allows you to query some common algorithms, such as bubble sort, sequential search, and so on. You can query the algorithm's description, time complexity, application scenarios, and implementation in some common languages with different parameters.\nTry: \n/query bubble sort \n/query bubble sort description \n/query bubble sort time \n/query bubble sort python"
        update.message.reply_text(replyMsg)
    else:
        mesString = context.args[0].lower()+context.args[1].lower()
        
        if(len(context.args)>=3):
            # Implementation = "$.." + context.args[2].lower() + "Implementation"
            list = []
            for index, msg in enumerate(context.args):
            # msgQ = context.args[0].lower().replace(" ","")
                if(msg.lower() == 'description'):
                    list.append('Description')
                    continue
                if(msg.lower() == 'time' or msg.lower() == 'complexity'):
                    list.append('TimeComplexity')
                    continue
                if(msg.lower() == 'application'or msg.lower() == 'scenarios'):
                    list.append('ApplicationScenarios')
                    continue
                else:
                    if(index>1):
                        list.append(msg.lower() + "Implementation")
            # msgQ = mesString
            print(mesString)
            print(list)
            for q in list:
                try:
                    # reply = redis1.get('testJson').decode('UTF-8')
                    # reply = redis1.json().get(mesString, q)
                    reply = mongoDB.readAlgorithm(mesString, q)
                    # reply = reply[0]
                    print(reply)
                    update.message.reply_text(reply)
                except (IndexError, ValueError):
                    update.message.reply_text('Sorry, this record is not currently in the database. Maybe you could try /GptON')
        else:
            # for msg in context.args:
            #     mesString += msg.lower()
            # msgQ = context.args[0].lower().replace(" ","")
            # msgQ = mesString
            # print(msgQ)
            try:
                # reply = redis1.get('testJson').decode('UTF-8')
                # reply = redis1.json().get(mesString, "$")
                reply = mongoDB.readAlgorithm(mesString, 'Description')
                # reply = reply[0]['Description']
                # print(reply)
                update.message.reply_text(reply)
            except (IndexError, ValueError):
                update.message.reply_text('Sorry, this record is not currently in the database. Maybe you could try /GptON')
    

def equiped_chatgpt(update, context, mes): 
    global chatgpt
    print('SUBMIT: '+ mes)
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
    msg = str(update)
    start = msg.find("'id': ") 
    end = msg.find(',', start)
    id = msg[start + 6:end]
    print(start)
    print(end)
    print(id)
    # try:
    #     msg = 'testMsg'
    #     reply = redis1.get(msg).decode('UTF-8')
    #     print(reply)
    #     update.message.reply_text(reply)
    # except (IndexError, ValueError):
    #     update.message.reply_text('Sorry, error in redis connection.')

# def add(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /add is issued."""
#     try:
#         global redis1
#         logging.info(context.args[0])
#         msg = context.args[0]   # /add keyword <-- this should store the keyword
#         redis1.incr(msg)
#         update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /add <keyword>')

# def hello_command(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /hello is issued."""
#     msg = context.args[0]
#     update.message.reply_text('Good day, \n'+ msg +'!')

def keywords(update: Update, context: CallbackContext):
    print(update.message.text)
    global GPTFlag
    if GPTFlag:
        equiped_chatgpt(update,context,update.message.text)
    msg = update.message.text.lower()
    resultJs = msg.find('javascript')
    resultJ = msg.find('java')
    resultPy = msg.find('python')
    resultC = msg.find('c ')
    resultCPP = msg.find('c++')
    resultCS = msg.find('c#')
    resultCSS = msg.find('css')
    resultHTML = msg.find('html')

    if(resultJ == resultJs):
        resultJ = -1

    keys = ['javascript','java','python','c','c++','c#','css','html']
    values = [resultJs,resultJ,resultPy,resultC,resultCPP,resultCS,resultCSS,resultHTML]
    results = dict(zip(keys,values))

    msg = str(update)
    start = msg.find("'id': ") 
    end = msg.find(',', start)
    id = msg[start + 6:end].strip()
    print(id)

    for key ,value in results.items():
        if (value > -1):
            update.message.reply_text('You just said the keywords '+key.upper()+' !')
            print(key)
            try:
                mongoDB.increaseLog(key,id)
                # redis1.incr(key)
                # update.message.reply_text()
                # print('You have said ' + key +  ' for ' + redis1.get(key).decode('UTF-8') + ' times.')
            except (IndexError, ValueError):
                update.message.reply_text('Sorry, error in mongoDB connection.')

    

def showStatistic(update: Update, context: CallbackContext)-> None:
    msg = str(update)
    start = msg.find("'id': ") 
    end = msg.find(',', start)
    id = msg[start + 6:end].strip()
    print(id)
    if(len(context.args)==0):
        replyMsg = "This function allows you to query the number of times keywords in each programming language have been mentioned in past chats.\nTry:\n/statistic all\n/statistic python\n/statistic javascript"
        update.message.reply_text(replyMsg)
    else:
        if(context.args[0].lower() == 'all'):
            dic = {'javascript':0,'java':0,'python':0,'c':0,'c++':0,'c#':0,'css':0,'html':0}
            max = -1
            maxName = 'none'
            replyMsg = 'You have said: \n'
            for key ,value in dic.items():
                # if (value > -1):
                #     print(key)
                try:
                    # value = redis1.get(key).decode('UTF-8')
                    value = mongoDB.queryLog(key,id)
                    print(value)
                    if(int(value) > int(max) ):
                        max = value
                        maxName = key
                        # redis1.incr(key)
                        # update.message.reply_text()
                    replyMsg +=  key +  ' for ' + str(value) + ' times;\n'
                    # print()
                except (IndexError, ValueError):
                    update.message.reply_text('Sorry, error in mongoDB connection.')
                    # print(IndexError)
                    # print(ValueError)
            if(max != -1 and max != 0):
                replyMsg += 'It seems like maybe ' + maxName.upper() +  ' is your favourite language.'
            else:
                replyMsg += 'It seems like maybe you dont have favourite language.'
        else:
            replyMsg = 'You have said '
            for key in context.args:
                # if (value > -1):
                #     print(key)
                try:
                    # value = redis1.get(key).decode('UTF-8')
                    value = mongoDB.queryLog(key,id)
                        # redis1.incr(key)
                        # update.message.reply_text()
                    replyMsg +=  key +  ' for ' + str(value) + ' times.\n'
                    # print()
                except (IndexError, ValueError):
                    update.message.reply_text('Sorry, error in mongoDB connection.')
        update.message.reply_text(replyMsg)
        # return

if __name__ == '__main__':
    main()
