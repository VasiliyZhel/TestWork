import telebot
import time
import random

# for bot
token = "6563887922:AAGSUQvRlodCLtOumSGHFoxWNAukFPDkatA"
bot = telebot.TeleBot(token)
# for reg
client_name = ""
organization = ""
role = ""
phone = ""
# fot ticket
topic = ""
full_topic = ""
prioritet = ""
# for users
list = {}
user_info = [client_name, organization, role, phone]
welcome_text = """
Привет, тебя приветствует бот техподдержки!
Чтоб оставить заявку жми /new_ticket
Чтоб зарегистрировать нового пользователя жми /reg
Чтоб увидеть список доступных команд жми /help
"""
welcome_text_for_user = """
С возвращением!
Чтоб оставить заявку жми /new_ticket
Чтоб увидеть список доступных команд жми /help
"""
help_text = """
Доступные команды:
/start - Перезапускает бота
/reg - Регистрирует нового пользователя
/new_ticket - Создает новую заявку
/show_me - Показывает регистрациоонные данные
"""


@bot.message_handler(commands=["start"])
def start(message):
    """
    Обработка команды start
    Если пользователь есть в списке, приветствует по имени
    """
    user_table = open('Users.txt', 'r', encoding="utf8")
    if str(message.from_user.id) in user_table.read():
        bot.send_message(message.from_user.id, welcome_text_for_user)
    else:
        bot.send_message(message.from_user.id, welcome_text)
    user_table.close()


@bot.message_handler(commands=["help"])
def start(message):
    "Обработка команды help"
    bot.send_message(message.from_user.id, help_text)


@bot.message_handler(commands=["show_me"])  # Декоратор для вывода регистрационных данных
def show_me(message):
    "Функция выводит пользователю его регистрационные данные"
    user_table = open('Users.txt', 'r', encoding="utf8")
    s = user_table.read()
    stroka = ""
    spiis = []
    if str(message.from_user.id) in s:
        for l in s.split("\n"):
            if str(message.from_user.id) in l:
                stroka = l
                spiis = stroka.split(",")
        #bot.send_message(message.from_user.id, stroka)
        bot.send_message(message.from_user.id, f"{spiis[1]}, {spiis[2]}, {spiis[3]}, {spiis[4]}")
    else:
        bot.send_message(message.from_user.id, f"Вы еще не прошли регистрацию \nЧтоб зарегистрировать нового пользователя жми /reg")
    user_table.close()


@bot.message_handler(commands=["reg"])  # Декоратор для регистрации пользователя
def get_name(message):
    "Функция запрашивает имя, если айди пользователя есть в списке, то выходит уведомляет об этом"
    user_table = open('Users.txt', 'r', encoding="utf8")
    if str(message.from_user.id) in user_table.read():
        bot.send_message(message.from_user.id, "Вы уже зарегистрированны")
    else:
        bot.send_message(message.from_user.id, "Введите свое имя")
        bot.register_next_step_handler(message, get_organisation)
    user_table.close()


def get_organisation(message):
    "Функция запрашивает организацию у клиента"
    global client_name
    client_name = message.text
    bot.send_message(message.from_user.id, "От какой огранизации вы обращаетесь?")
    bot.register_next_step_handler(message, get_role)


def get_role(message):
    "Функция запрашивает должность"
    global organization
    organization = message.text
    bot.send_message(message.from_user.id, "Введите свою должность?")
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    "Функция запрашивает номер телефона"
    global role
    role = message.text
    bot.send_message(message.from_user.id, "Введите номер телефона для связи")
    bot.register_next_step_handler(message, send_admin_reg)


def send_admin_reg(message):
    "Функция отправляет уведомляет пользователя о регистрации пользователя и отправляет данные админу, выводит в лог, так же добавляет пользователя в файл"
    global phone
    phone = message.text
    bot.send_message(message.from_user.id,
                     "Регистрация завершена, теперь вы можете создавать заявки. Чтоб создать заявку жми /new_ticket \nЧтоб увидеть список доступных команд жми /help")
    # Создали переменную айди и переменную с информацией о пользователе, добавили в словарь
    a = message.from_user.id
    b = f"{client_name}, {organization}, {role}, {phone}"
    global list
    list[a] = b
    user_table = open('Users.txt', 'a', encoding="utf8")
    for key, value in list.items():
        user_table.write(f'{key}, {value},\n')
    user_table.close()
    bot.send_message(1362233196, list.get(message.from_user.id))
    bot.send_message(1362233196, message.from_user)


@bot.message_handler(commands=["new_ticket"])  # Декоратор для создания заявок
def get_ticket(message):
    "Функция запрашивает описание заявки и отправляет на регистрацию, если пользователя нет в базе"
    user_table = open('Users.txt', 'r', encoding="utf8")
    if str(message.from_user.id)  not in user_table.read():
        bot.send_message(message.from_user.id, "Чтоб создавать заявки требуется пройти регистрацию, жми /reg")
    else:
        bot.send_message(message.from_user.id, "Введите название заявки")
        bot.register_next_step_handler(message, get_full_ticket)
    user_table.close()

def get_full_ticket(message):
    "Функция запрашивает полное описание заявки"
    global topic
    topic = message.text
    bot.send_message(message.from_user.id, "Опишите проблему")
    bot.register_next_step_handler(message, get_status)


def get_status(message):
    "Функция запрашивает приоритет"
    global full_topic
    full_topic = message.text
    bot.send_message(message.from_user.id, "Введите приоритет заявки")
    bot.register_next_step_handler(message, send_admin_ticket)


def send_admin_ticket(message):
    global prioritet
    prioritet = message.text
    bot.send_message(message.from_user.id, "Заявка создана, свяжемся с вами в ближайшее время")
    bot.send_message(1362233196, f"{topic}, {full_topic}, {prioritet}")
    user_table = open('Users.txt', 'r', encoding="utf8")
    s = user_table.read()
    stroka = ""
    spiis = []
    if str(message.from_user.id) in s:
        for l in s.split("\n"):
            if str(message.from_user.id) in l:
                stroka = l
                spiis = stroka.split(",")
        #bot.send_message(message.from_user.id, stroka)
        bot.send_message(1362233196, f"{spiis[1]}, {spiis[2]}, {spiis[3]}, {spiis[4]}")
    else:
        bot.send_message(1362233196, f"Случилась хуйня при создании заявки ")
    user_table.close()


@bot.message_handler(content_types=["text"]) # Декоратор обработки неизвестных сообщений
def read_text(message):
    "Функция присылает ответ на неизвестные команды"
    bot.send_message(message.from_user.id, "Я тебя не понимаю, жми /help")


bot.polling()