# импортируем все необходимые библиотеки и т.п.
from requirements import *
# создаем экземпляр класса с запросами к API
pf = PetFriends()


# получаем ключ авторизации, доступный в каждом тесте
@pytest.fixture(autouse=True)
def auth_key_api():
    global auth_key
    _, auth_key, _ = pf.get_api_key(valid_email, valid_password)
    return auth_key


# показываем длительность теста
@pytest.fixture(autouse=True)
def time_delta(request):
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print (f"\nТест {request.function.__name__} длился: {end_time - start_time}")


# параметризация - один тест на несколько тестовых данных
# функция generate_string(n) генерирует строку длиной n
@pytest.mark.parametrize("name"
   , [generate_string(255), generate_string(1001), russian_chars(),
      russian_chars().upper(), chinese_chars(),
      special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian',
          'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
   , [generate_string(255), generate_string(1001), russian_chars(),
      russian_chars().upper(), chinese_chars(),
      special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian',
          'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
def test_successful_update_self_pet_info(name, animal_type, age):
    """Позитивные кейсы обновления информации"""
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
        raise Exception("There is no my pets")


@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                        ['', '-1', '0', '100', '1.5', '2147483647', '2147483648',
                         special_chars(), russian_chars(),
                         russian_chars().upper(), chinese_chars()]
   , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max',
          'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
def test_unsuccessful_update_self_pet_info(name, animal_type, age):
    """Негативные кейсы обновления информации"""
    # обращаемся к методу класса из файла api, передав ключ авторизации из фикстуры
    # и получаем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")
    # если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result, res = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 400
        assert result['name'] == name
        return res
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# тут не подобрать очевидных параметров
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    # обращаемся к методу класса из файла api, передав ключ авторизации из фикстуры
    # и получаем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")
    # проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")
    # берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _, res = pf.delete_pet(auth_key, pet_id)
    # ещё раз запрашиваем список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")
    # проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    return res