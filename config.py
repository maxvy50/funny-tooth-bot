import os

import telebot

from enum import Enum

token = "511300784:AAGqpH9DZtSfbLhYzklmbLXk46-Pi_LL388"

db_file = os.path.dirname(os.path.abspath(__file__)) + "database.vdb"
age_db_file = os.path.dirname(os.path.abspath(__file__)) + "age_database.vdb"
picsdir = os.path.dirname(os.path.abspath(__file__)) + '/pics/'

yes = {'Да', 'да', 'ага', 'готов', 'Готов', 'Ага', 'Ок', 'ок', 'ОК', 'ДА'}
no = {'Нет', 'Неа', 'нет', 'не', 'не готов', 'Не готов'}


###### keyboards
default_markup = telebot.types.ReplyKeyboardRemove()
######
binary_markup = telebot.types.ReplyKeyboardMarkup()
yes_button = telebot.types.KeyboardButton('Да')
no_button = telebot.types.KeyboardButton('Нет')
binary_markup.row(yes_button, no_button)
######
puyol_markup = telebot.types.ReplyKeyboardMarkup()
key1 = telebot.types.KeyboardButton('Пуйоль Карлес')
key2 = telebot.types.KeyboardButton('Пуйоль Кариес')
key3 = telebot.types.KeyboardButton('Пуйоль Конгресс')
key4 = telebot.types.KeyboardButton('Пуйоль Компресс')
puyol_markup.row(key1, key2)
puyol_markup.row(key3, key4)
######

def keyword(age) -> list:
    if age in range(1, 6):
        return ['Кариес', 'Микробы']
    elif age in range(6, 8):
        return ['Молочный', 'Бяка']
    elif age in range(8, 10):
        return ['Эмаль', 'Фтор']
    elif age in range(10, 12):
        return ['Десна', 'Зуб']
    elif age in range(12, 14):
        return ['Зубная', 'Монстр']
    elif age in range(14, 16):
        return ['Паста', 'Фрукт']
    elif age in range(16, 18):
        return ['Фея', 'Творог']
    elif age in range(18, 20):
        return ['Зубастик', 'Кола']
    elif age in range(20, 22):
        return ['Кальций', 'Пломба']
    elif age in range(22, 24):
        return ['Брекеты', 'Врач']
    elif age in range(24, 26):
        return ['Яблоко', 'Ортодонт']
    elif age in range(26, 31):
        return ['Флосс', 'Мудрость']
    elif age in range(31, 41):
        return ['Гигиена', 'Ксилит']
    elif age > 40:
        return ['Стоматолог', 'Доктор']


class States(Enum):

    START = "start"
    OFFERING = "offering"
    KEYWORD_REQUEST = "waiting for keyword"
    READINESS_ACCEPTANCE = "readiness acceptance"
    ITS_ALL_OVER = 'dialog was interrupted'
    AGE_REQUEST = 'age request'
    READY = 'start to interact'
    RULE1 = 'puyol question'
    RULE2 = 'hygiene question'
    RULE3 = 'brush question'
    RULE4 = 'tooth paste question'
    RULE5 = 'facts'
    RULE6 = 'a garlic'
    RULE7 = 'to prevent'
    RULE8 = 'an inspection'
    RULE9 = 'awful behaviour'
    RULE10 = 'brackets'
    FINISH_HIM = 'its all over'
    THE_END = 'dialog was ended'
    SLACK = 'slackerbot'

