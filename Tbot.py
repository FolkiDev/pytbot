# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
import telebot
import os
import random
updater = Updater(token='458063962:AAHlnAveA65x66JeBTr5eOedCSJEXVnhfY0') # Токен к Telegram
dispatcher = updater.dispatcher

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='\U0000270B Привет, я бот Пончик! \U0001F369 \n' '\U00002709 Давай пообщаемся? \U0000270F')
    
def helpCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='\U0001F4C3 Команды (Пишутся БЕЗ ковычек): \U0001F4C3 \n \U000027A1 "гифка котик" - бот пришлет вам гифку с котиком \n \U000027A1 "фото котиков" - бот пришлет вам фото с котиками')
def musicCommand(bot, update) :
    directory = 'C:\music'
    all_files_in_directory = os.listdir(directory)
    print(all_files_in_directory)
    random_file = random.choice(all_files_in_directory)
    music = open(directory + '/' + random_file, 'rb')
    bot.send_chat_action(update.message.from_user.id, 'upload_audio')
    bot.send_audio(update.message.from_user.id, music)
    music.close()
    bot.send_message(chat_id=update.message.chat_id, text='Когда находишь музыку под настроение, понимаешь, что не так уж и много нужно для счастья.')

def textMessage(bot, update):
    request = apiai.ApiAI('b9cd309ff2194c12a5c1e9e4dfc265bc').text_request() # Токен к Dialogflow
    request.lang = 'ru'
    request.session_id = 'Ponchickbot'
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']

    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Незнаю что и ответить то.')

start_command_handler = CommandHandler('start', startCommand)
help_command_handler = CommandHandler('help', helpCommand)
music_command_handler = CommandHandler('music', musicCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(music_command_handler)
dispatcher.add_handler(help_command_handler)
dispatcher.add_handler(text_message_handler)
updater.start_polling(clean=True)
updater.idle()