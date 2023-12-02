from telebot.types import WebAppInfo
from telebot import TeleBot, types
import requests
import json
from telegram_bot_pagination import InlineKeyboardPaginator

TOKEN = '6825517872:AAEh9gngk1C6MSMAULl5VIYOHynvpxcS5zM'
bot = TeleBot(TOKEN)
questions_link = 'http://127.0.0.1:5000/questions_bot'
not_answer_questions_link = 'http://127.0.0.1:5000/not_answer_questions_bot'
send_question_link = 'http://127.0.0.1:5000/send_question_bot'
teachers_link = 'http://127.0.0.1:5000/teachers_bot'
student_link = 'http://127.0.0.1:5000/student_bot'
register_html_link = 'https://mannopboy.github.io/register_bot/'
login_link = 'http://127.0.0.1:5000/login_bot'
status_teacher = {
    'status': False,
    'id': None
}
user = {
    'user_id': None,
    'username': None,
    'telegram_user_name': None,
    'role': None,
    'status': False
}
status = False
teacher_list = []
student_list = []
response_teacher = requests.get(teachers_link)
response_student = requests.get(student_link)
for teacher in response_teacher.json()['teachers']:
    teacher_list.append(teacher)
for student in response_student.json()['students']:
    student_list.append(student)


def buttons():
    if user['status'] and user['role'] == 'admin':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_first = types.KeyboardButton('Questions')
        button_second = types.KeyboardButton('Send question')
        button_three = types.KeyboardButton('Teachers')
        button_four = types.KeyboardButton('Students')
        button_five = types.KeyboardButton('Login', web_app=WebAppInfo(url=register_html_link))
        markup_reply.row(button_first, button_second, button_three, button_four, button_five)
    elif user['status'] and user['role'] == 'teacher':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_first = types.KeyboardButton('Questions')
        button_second = types.KeyboardButton('Not answer questions')
        button_three = types.KeyboardButton('Login', web_app=WebAppInfo(url=register_html_link))
        markup_reply.row(button_first, button_second, button_three)
    elif user['status'] and user['role'] == 'student':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_first = types.KeyboardButton('Questions')
        button_second = types.KeyboardButton('Send question')
        button_three = types.KeyboardButton('Login', web_app=WebAppInfo(url=register_html_link))
        markup_reply.row(button_first, button_second, button_three)
    else:
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_first = types.KeyboardButton('Login', web_app=WebAppInfo(url=register_html_link))
        button_second = types.KeyboardButton('Register')
        markup_reply.row(button_first, button_second)
    return markup_reply


@bot.message_handler(commands=['start'])
def start(massage):
    # name = massage.from_user
    markup_reply = buttons()
    bot.send_message(massage.chat.id, "Salam aleykum", reply_markup=markup_reply)


@bot.message_handler(content_types=['web_app_data'])
def callback(massage):
    json_user = json.loads(massage.web_app_data.data)
    info = {
        'name': json_user['name'],
        'telegram_name': massage.from_user.username,
        'password': json_user['password']
    }
    response = requests.post(login_link, json=info)
    if response.json()['status']:
        user['user_id'] = response.json()['id']
        user['username'] = info['name']
        user['telegram_user_name'] = info['telegram_name']
        user['role'] = response.json()['role']
        user['status'] = True
        markup_reply = buttons()
        bot.send_message(massage.chat.id, f"Registratsiya bo'ldingiz", reply_markup=markup_reply)
    else:
        user['user_id'] = None
        user['username'] = None
        user['telegram_user_name'] = None
        user['role'] = None
        user['status'] = False
        markup_reply = buttons()
        bot.send_message(massage.chat.id, f"Registratsiya bo'lmadingiz qayta urining", reply_markup=markup_reply)


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
    elif text == 'teachers' and not status and user['role'] == 'admin':
        for teacher in teacher_list:
            bot.send_message(massage.chat.id, f"{teacher['name']}")
    elif text == 'students' and not status and user['role'] == 'admin':
        for student in student_list:
            bot.send_message(massage.chat.id, f"{student['name']}")
    elif text == 'not answer questions' and not status and user['role'] == 'teacher':
        not_answer_question_list = []
        response_not_answer_questions = requests.get(not_answer_questions_link, json={
            'username': user['username']
        })
        for question in response_not_answer_questions.json()['questions']:
            not_answer_question_list.append(question)
        if not_answer_question_list:
            for question in not_answer_question_list:
                bot.send_message(massage.chat.id,
                                 f"Question: {question['question']} Student_name: {question['student_name']}")
        else:
            bot.send_message(massage.chat.id, f"Savol yo'q")
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
                'student_id': user['user_id'],
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
            markup_reply = buttons()
            bot.send_message(massage.chat.id, text, reply_markup=markup_reply)


bot.polling(none_stop=True, interval=0)
