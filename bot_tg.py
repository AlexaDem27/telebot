import telebot
import main

token = '6860502940:AAEfoGcdioz1d2idNGYu9UMXdBU4fZL3inY'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    """
    Бот реагирует на команду '/start'. Выводится информация о правильном синтаксисе ввода запроса   
    """
    bot.send_message(message.chat.id, 'Введите исполнителя / исполнителя и песню разделяя " ; " (пробелы обязательны!!! :). Подборка рекомендаций может занять некоторое время....')


@bot.message_handler(content_types='text')
def get_message(message):
    """
    Бот реагирует на текстовые сообщения.
    Аргумент: 
        message: text message
    """
    reccommend_lst = main.recom_music(message.text)
    print(reccommend_lst)
    try:
        bot.send_message(message.chat.id, 'Список рекомендаций:')
        for i in reccommend_lst:
            bot.send_message(message.chat.id, i)
    except:
        bot.send_message(message.chat.id, "dont worry")


bot.polling(none_stop=True, interval=0)