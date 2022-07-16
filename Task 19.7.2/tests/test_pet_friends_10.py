from Module_19.api import PetFriends
from Module_19.settings import valid_email, valid_password
import os

pf = PetFriends()

#тест-кейс 1

import random
import string

#генерируем случайную строку на основе длины, которую мы передаем функции
def generate_random_string(length):
    #string.ascii_letters включает все строчные и прописные буквы латиницы
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def test_add_new_pet_with_huge_name(name=generate_random_string(1000), animal_type='белка',
                                     age='3', pet_photo='images/P1040103.jpg'):
    """Проверяем, примет ли сервер имя, состоящее из 1000 букв"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#тест-кейс 2

def test_add_new_pet_with_huge_data(name=generate_random_string(1000), animal_type=generate_random_string(1000),
                                     age=generate_random_string(1000), pet_photo='images/P1040103.jpg'):
    """Проверяем, примет ли сервер данные, состоящие из 1000 букв"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#тест-кейс 3

def test_add_new_pet_with_empty_name(name='', animal_type='белка',
                                     age='3', pet_photo='images/P1040103.jpg'):
    """Проверяем, примет ли сервер пустое имя"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#тест-кейс 4

def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем наличие ошибки при запросе списка животных с указанием неверного ключа авторизации """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    #задаем неверный ключ
    auth_key = {"key": "2bc5965f75bebd01659b568d2ac329429357e3570c38f0c09e82fb41"}
    status, result = pf.get_list_of_pets(auth_key, filter)

    #ошибка - пользователь не найден
    assert status == 403

#тест-кейс 5

def test_unsuccessful_add_empty_photo(pet_photo='images/void.jpg'):
    """Проверяем загрузку пустого фото (просто файл с расширением jpg)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем загрузить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 500 - ошибка при обработке изображения сервером
        assert status == 500
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#тест-кейс 6

def test_successful_add_one_pixel_photo(pet_photo='images/1px.jpg'):
    """Проверяем загрузку фото с разрешением 1Х1 пикселей"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем загрузить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 (ошибок нет)
        assert status == 200
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#тест-кейс 7

def test_successful_add_10kX10k_pixel_photo(pet_photo='images/10kX10k.jpg'):
    """Проверяем загрузку фото с разрешением 10 000 Х 10 000 пикселей"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем загрузить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 (ошибок нет)
        assert status == 200
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#тест-кейс 8

def test_add_new_pet_with_empty_data(name='', animal_type='',
                                     age='', pet_photo='images/P1040103.jpg'):
    """Проверяем, примет ли сервер фото и пустые поля"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#тест-кейс 9

def test_add_new_pet_without_photo_with_empty_data(name='', animal_type='', age=''):
    """Проверяем, примет ли сервер пустые данные"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#тест-кейс 10

import requests
def test_delete_pets_of_another_person():
    """Проверяем возможность удаления чужого питомца"""

    #получаем ключ авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    #передаем ключ в заголовки
    headers = {'auth_key': auth_key['key']}
    #получаем всех животных с главной страницы сайта, передав заголовки
    res = requests.get('https://petfriends.skillfactory.ru/api/pets', headers=headers)
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text

    #удаляем самого первого питомца
    pet_id = result['pets'][0]['id']
    res_1 = requests.delete('https://petfriends.skillfactory.ru/api/pets/' + pet_id, headers=headers)

    status = res_1.status_code

    #получаем НОВЫЙ СПИСОК всех животных с главной страницы сайта, передав заголовки
    res = requests.get('https://petfriends.skillfactory.ru/api/pets', headers=headers)
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    #Проверяем, что id удаленного животного не равно id первого животного из нового списка
    if pet_id != result['pets'][0]['id']:
        assert status == 200
    else:
        raise Exception("Failed to delete a pet")
