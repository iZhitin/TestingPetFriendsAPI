# импортируем библиотеку для тестирования
import pytest
# импортируем библиотеку для формирования пути к файлу фотографии
import os
# импортируем библиотеку для определения времени прохождения теста
from datetime import datetime

# импортируем класс из соседнего файла с методами для обращения к API
from api import PetFriends
# импортируем данные авторизации из соседнего файла
from settings import valid_email, valid_password

# не используется
# import logging
# logger = logging.getLogger()

# создадим экземпляр класса с удобной переменной
pf = PetFriends()


# фикстура возвращает ключ авторизации и делает его доступным для ВСЕХ тестов этого файла
@pytest.fixture(autouse=True)
def auth_key_api():
    global auth_key
    _, auth_key, _ = pf.get_api_key(valid_email, valid_password)
    return auth_key


# фикстура определяет и возвращает время прохождения для ВСЕХ тестов этого файла
@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print (f"\nТест шел: {end_time - start_time}")


# фикстура логирует и возвращает данные запросов и ответов для ВСЕХ тестов этого файла
# благодаря request мы можем сослаться на все функции в коде
@pytest.fixture(autouse=True)
def logger(request):
    yield
    request.function().request.encoding = 'utf-8'
    request.function().encoding = 'utf-8'
    with open('log.txt', 'a', encoding='utf8') as logFile:
        logFile.write(
        # название функции (теста)
        f'T1: {request.function.__name__}\n' \
        f'ЗАПРОС:\n' \
        f' Метод запроса:\n' \
        f' {str(request.function().request.method)}\n' \
        f' Заголовки запроса:\n' \
        f' {str(request.function().request.headers)}\n' \
        f' Параметры пути запроса:\n' \
        f' {str(request.function().request.params)}\n' \
        f' Параметры строки запроса:\n' \
        f' {str(request.function().request.data)}\n' \
        f' Тело запроса:\n' \
        f' {str(request.function().request.text)}\n' \
        f'ОТВЕТ:\n' \
        f' Код ответа:\n' \
        f' {str(request.function().status_code)}\n' \
        f' Тело ответа:\n' \
        f' {(str(request.function().text))}\n\n' \
        )
    print('Лог теста записан в log.txt\n\n')


# маркировка теста двумя маркерами api и get
@pytest.mark.api
@pytest.mark.get
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что запрос API ключа возвращает статус 200 и в результате содержится слово key"""

    # обращаемся к методу класса из файла api
    status, result, res = pf.get_api_key(email, password)

    # cверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result
    return res


# маркировка теста двумя маркерами api и get
@pytest.mark.api
@pytest.mark.get
def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
    Доступное значение параметра filter - 'my_pets' либо '' """

    # обращаемся к методу класса из файла api, передав ключ авторизации из фикстуры
    # и пустой фильтр, чтобы получить список всех животных сайта
    status, result, res = pf.get_list_of_pets(auth_key, filter)

    # cверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert len(result['pets']) > 0
    return res


# маркировка теста тремя маркерами api, post и photo
@pytest.mark.api
@pytest.mark.post
@pytest.mark.photo
def test_add_new_pet_with_valid_data(name='Doppleganger', animal_type='собака',
                                     age='4', pet_photo='images/P1040103.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # обращаемся к методу класса из файла api, передав ключ авторизации из фикстуры
    status, result, res = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    return res


# маркировка теста двумя маркерами api и post
@pytest.mark.api
@pytest.mark.post
def test_add_new_pet_without_photo(name='все-равно', animal_type='просто собака без фото',
                                     age='1'):
    """Проверяем, что можно добавить питомца с корректными данными без ФОТО"""

    # обращаемся к методу класса из файла api, передав ключ авторизации из фикстуры
    status, result, res = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    return res


# маркировка теста двумя маркерами api и delete
@pytest.mark.api
@pytest.mark.delete
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # обращаемся к методу класса из файла api, передав ключ авторизации из фикстуры
    # и получаем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")

    # проверяем - если список своих питомцев пустой,
    # то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")

    # берём id первого питомца из списка и отправляем запрос на удаление
    # значение первого объекта в словаре pets с ключом id
    pet_id = my_pets['pets'][0]['id']
    status, _, res = pf.delete_pet(auth_key, pet_id)

    # ещё раз запрашиваем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")

    # проверяем что статус ответа равен 200 и в списке (словаре) питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    return res


# маркировка теста двумя маркерами api и put
@pytest.mark.api
@pytest.mark.put
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=10):
    """Проверяем возможность обновления информации о питомце"""

    # обращаемся к методу класса из файла api, передав ключ авторизации из фикстуры
    # и получаем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")

    # если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result, res = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        return res
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no any my pets at all")


# маркировка теста тремя маркерами api, post и photo
@pytest.mark.api
@pytest.mark.post
@pytest.mark.photo
def test_successful_add_photo(pet_photo='images/P1040103.jpg'):
    """Проверяем, что можно добавить ТОЛЬКО ФОТО"""

    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # обращаемся к методу класса из файла api, передав ключ авторизации из фикстуры
    # и получаем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")

    # если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result, res = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        return res
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no any my pets at all")
