import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Я Бот-Конвертер валют и я могу:  \n- Показать список доступных валют /values \
    \n- Сделать конвертацию валюты, для этого введите команду в формате <имя валюты цену котой хотите узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>\n \
- Инструкция по использованию бота /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию введите команду в следующем формате: \n<имя валюты цену котой хотите узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>\n/values'
    bot.reply_to(message, text)



@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException("Слишком много параметров.")
        elif len(values) < 3:
            raise APIException("Мало параметров.")

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()



