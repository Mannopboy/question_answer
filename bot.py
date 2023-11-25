from telebot.types import WebAppInfo
from telebot import TeleBot, types
import requests

TOKEN = '6825517872:AAEh9gngk1C6MSMAULl5VIYOHynvpxcS5zM'
bot = TeleBot(TOKEN)
questions_link = 'http://127.0.0.1:5000/questions_bot'


@bot.message_handler(commands=['start'])
def start(massage):
    # name = massage.from_user
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_first = types.KeyboardButton('Questions')
    button_second = types.KeyboardButton('Send question')
    button_three = types.KeyboardButton('Register', web_app=WebAppInfo(url='https://127.0.0.1:5000/login'))
    markup_reply.row(button_first, button_second, button_three)
    bot.send_message(massage.chat.id, "Salam aleykum", reply_markup=markup_reply)


# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     if call.data == 'yes':
#         name = call.from_user.first_name
#         user = get_user(name)
#         if not user:
#             register_user(name, False)
#             bot.send_message(call.message.chat.id, "Botga registratsiya bo'ldingiz. Botni ishlatishingiz munkin !!!")
#             bot.send_message(call.message.chat.id, "Ildiz ostidan chiqarmoqchi bo'lgan soningizni yuboring.")
#     elif call.data == 'no':
#         bot.send_message(call.message.chat.id, "Bot faoliyati tugatildi")
#         bot.send_message(call.message.chat.id, "Bot qayta ishga tushirish uchun /start buyrug'ini yuboring")
#     elif call.data == 'users':
#         users = get_users()
#         info = ''
#         for user in users:
#             info += f'Index: {users.index(user) + 1} Name: {user[1]}   '
#         bot.delete_message(call.message.chat.id, call.message.message_id)
#         bot.send_message(call.from_user.id, info)


@bot.message_handler()
def massage(massage):
    text = massage.text.lower()
    if text == 'questions':
        response = requests.get(questions_link)
        number = 0
        for question in response.json()['questions']:
            number += 1
            bot.send_message(massage.chat.id,
                             f"<strong>Question:</strong> {question['question_text']} <strong>Answer:</strong> {question['answer_text']}",
                             parse_mode='html')
    elif text == 'send question':
        bot.send_message(massage.chat.id, f'Ok')
    else:
        bot.send_message(massage.chat.id, f'{text}')


bot.polling(none_stop=True, interval=0)
