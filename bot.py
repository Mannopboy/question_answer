from telebot.types import WebAppInfo, WebAppData
from telebot import TeleBot, types
import requests
from telegram_bot_pagination import InlineKeyboardPaginator

TOKEN = '6825517872:AAEh9gngk1C6MSMAULl5VIYOHynvpxcS5zM'
bot = TeleBot(TOKEN)
questions_link = 'http://127.0.0.1:5000/questions_bot'
send_question_link = 'http://127.0.0.1:5000/send_question_bot'
teachers_link = 'http://127.0.0.1:5000/teachers_bot'
status_teacher = {
    'status': False,
    'id': None
}
status = False
teacher_list = []
response = requests.get(teachers_link)
for teacher in response.json()['teachers']:
    teacher_list.append(teacher)


def buttons():
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_first = types.KeyboardButton('Questions')
    button_second = types.KeyboardButton('Send question')
    button_three = types.KeyboardButton('Register')
    markup_reply.row(button_first, button_second, button_three)
    return markup_reply


@bot.message_handler(commands=['start'])
def start(massage):
    # name = massage.from_user
    markup_reply = buttons()
    bot.send_message(massage.chat.id, "Salam aleykum", reply_markup=markup_reply)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 1:
        # name = call.from_user.first_name
        bot.send_message(call.message.chat.id, "Botga registratsiya bo'ldingiz. Botni ishlatishingiz munkin !!!")


@bot.message_handler()
def massage(massage):
    text = massage.text.lower()
    global status
    global status_teacher
    if text == 'questions' and not status:
        response = requests.get(questions_link)
        number = 0
        for question in response.json()['questions']:
            number += 1
            bot.send_message(massage.chat.id,
                             f"<strong>Question:</strong> {question['question_text']} <strong>Answer:</strong> {question['answer_text']}",
                             parse_mode='html')
    elif text == 'send question' and not status:
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for teacher in teacher_list:
            button = types.KeyboardButton(f"{teacher['name']}")
            markup_reply.row(button)
        bot.send_message(massage.chat.id, f"O'qtuvchi tanlang", reply_markup=markup_reply)
    else:
        for teacher in teacher_list:
            if teacher['name'] == text.capitalize():
                status = True
                status_teacher['id'] = teacher['id']
        if status:
            status_teacher['status'] = True
            status = False
            bot.send_message(massage.chat.id, f"O'qtuvchiga savol yuboring")
        elif status_teacher['status']:
            status_teacher['status'] = False
            markup_reply = buttons()
            info = {
                'teacher_id': status_teacher['id'],
                'question': text
            }
            response = requests.post(send_question_link, json=info)
            if response.json()['status']:
                bot.send_message(massage.chat.id, f"O'qtuvchiga savol yuborildi", reply_markup=markup_reply)
            else:
                bot.send_message(massage.chat.id, f"Savol yuborishda hatolik yuz berdi", reply_markup=markup_reply)
        else:
            status_teacher['status'] = False
            status = False
            bot.send_message(massage.chat.id, text)


bot.polling(none_stop=True, interval=0)
