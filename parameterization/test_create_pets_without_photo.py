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
    print(f"\nТест {request.function.__name__} длился: {end_time - start_time}")


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
def test_add_new_pet_simple_positive(name, animal_type,
                           age):
    """Положительные тесты с валидными параметрами"""
    # добавляем питомца
    pytest.status, result, _ = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    # сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


# в функции валидации возраста больше нет нужды, так как появился отдельный тестовый набор негативных сценариев
@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                        ['', '-1', '0', '100', '1.5', '2147483647', '2147483648',
                         special_chars(), russian_chars(),
                         russian_chars().upper(), chinese_chars()]
   , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max',
          'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_simple_negative(name, animal_type,
                           age):
    """Негативные тесты с невалидными параметрами"""
    # добавляем питомца
    pytest.status, result, _ = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    # сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 400
