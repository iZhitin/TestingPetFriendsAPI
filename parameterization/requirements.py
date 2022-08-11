# импортируем необходимые библиотеки
import os
import pytest
import requests
from datetime import datetime

# импортируем класс из файла API
from api import PetFriends

# импортируем данные авторизации из файла settings
from settings import valid_email, valid_password


# необходимые функции
def generate_string(n):
    return "x" * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


# Здесь мы взяли 20 популярных китайских иероглифов
def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


# не работает
# ЛОГИРОВАНИЕ (благодаря request мы можем сослаться на все функции в коде)
# @pytest.fixture(autouse=True)
# def logger(request):
#     yield
#     # request.function().request.encoding = 'utf-8'
#     # request.function().encoding = 'utf-8'
#     with open('log.txt', 'a', encoding='utf8') as logFile:
#         logFile.write(
#         f'T1: {request.function.__name__}\n' \
#         f'ЗАПРОС:\n' \
#         f' Метод запроса:\n' \
#         f' {str(request.function().request.method)}\n' \
#         f' Заголовки запроса:\n' \
#         f' {str(request.function().request.headers)}\n' \
#         f' Параметры пути запроса:\n' \
#         f' {str(request.function().request.params)}\n' \
#         f' Параметры строки запроса:\n' \
#         f' {str(request.function().request.data)}\n' \
#         f' Тело запроса:\n' \
#         f' {str(request.function().request.text)}\n' \
#         f'ОТВЕТ:\n' \
#         f' Код ответа:\n' \
#         f' {str(request.function().status_code)}\n' \
#         f' Тело ответа:\n' \
#         f' {(str(request.function().text))}\n\n' \
#         )
#     print('Лог теста записан в log.txt\n\n')
