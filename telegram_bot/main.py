# You can take token by using a @BotFather
from telegram_token import token
from config import reply_texts
from model import ClassPredictor
import telebot
from io import BytesIO


class_ = ClassPredictor()
bot = telebot.TeleBot(token, threaded=False)

def te_find(message):
    name, surname = message.from_user.first_name, message.from_user.last_name
    if name == None:
        if surname == None:
            te = '-'
        else:
            te = surname
    else:
        if surname == None:
            te = name
        else:
            te = '{} {}'.format(surname, name)
    return te

@bot.message_handler(commands=['start'])
def start(message):
    person = te_find(message)
    start_text = reply_texts['start_text'].format('' if person == '-' else f', {person}')
    bot.send_message(message.chat.id, start_text)   
        
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, reply_texts['help_text'])       
        
def prediction(photo, type_):
    if type_ == 'd':
        file_id = photo.file_id
    else:
        file_id = photo[2].file_id

    photo = telebot.apihelper.download_file(token, telebot.apihelper.get_file(token, file_id)['file_path'])
    photo = BytesIO(photo)

    output = class_.predict(photo)
    return output
  
@bot.message_handler(content_types=["photo"])
def photos(message):
    ph = message.photo
    output = prediction(ph, 'ph')
    bot.send_message(message.chat.id, reply_texts['pred_answer'].format(output))
        
@bot.message_handler(content_types=["document"])
def documents(message):
    ph = message.document
    output = prediction(ph, 'd')
    bot.send_message(message.chat.id, reply_texts['pred_answer'].format(output))
        
@bot.message_handler(content_types=["text"])
def texts(message):
    bot.send_message(message.chat.id, reply_texts['not_understand'])


def main():
    bot.polling(none_stop = True, interval = 0)

if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            sleep(1)
