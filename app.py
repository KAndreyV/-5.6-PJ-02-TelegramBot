import telebot
from config import TOKEN, keys
from extensions import APIException, ValueConventer


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту, разделяя данные пробелом, в следующем формате:\n<имя валюты из \
какой переводим> \
<в какую валюту переводим> \
<колличество переводимой валюты>\nВсе доступные валюты: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types = ['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = ValueConventer.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()