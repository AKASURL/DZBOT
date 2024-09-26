import telebot
import urllib.request
import json


TOKEN = '7760579200:AAFeJTJ9RpouWYwJJsUfxEFHQh2jk7-DeM0'
CBU_API_URL = "https://cbu.uz/ru/arkhiv-kursov-valyut/json/"


bot = telebot.TeleBot(TOKEN)


def get_currency_rate(currency_code):
    with urllib.request.urlopen(CBU_API_URL) as response:
        data = response.read().decode('utf-8')
        rates = json.loads(data)


        for item in rates:
            if item['Ccy'] == currency_code.upper():
                return float(item['Rate'])
    return None


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, " Я конвертер валют Введите команду в формате /convert <сумма> <валюта> ")


@bot.message_handler(commands=['convert'])
def convert(message):
    try:
        _, amount, currency = message.text.split()
        amount = float(amount)
        rate = get_currency_rate(currency)

        if rate:
            converted_amount = amount * rate
            bot.send_message(message.chat.id, f"{amount} UZS = {converted_amount} {currency.upper()}")
        else:
            bot.send_message(message.chat.id, "информация о валюте недоступна.")
    except (ValueError, IndexError):
        bot.send_message(
            message.chat.id,
            "ОПАСНОСТЬ! Критическое повреждение системы.\n"
            "Критическое повреждение физического состояния.\n"
            "Критическое повреждение ментального здоровья.\n"
            "Вывод системы: немедленное прекращение операций.\n"
            "Активация аварийного режима восстановления.\n"
            "Требуется экстренная помощь для стабилизации состояния."
        )


if __name__ == '__main__':
    bot.polling(none_stop=True)