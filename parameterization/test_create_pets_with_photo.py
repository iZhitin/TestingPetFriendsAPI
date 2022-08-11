# импортируем все необходимые библиотеки и т.п.
from requirements import *
# создаем экземпляр класса с запросами к API
pf = PetFriends()


# получаем ключ авторизации
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


@pytest.mark.parametrize("name"
   , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
      special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
   , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
      special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
@pytest.mark.parametrize("pet_photo", ['images/P1040103.jpg', 'images/1.bmp', 'images/1px.jpg', 'images/10kX10k.jpg', 'images/cat1.gif', 'images/cat1.png'], ids=['image.jpg', 'image.bmp', '1px', '10kX10k', 'image.gif', 'image.png'])
def test_add_new_pet_positive(name, animal_type,
                           age, pet_photo):
    """ Положительные тесты с валидными параметрами """
    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # добавляем питомца
    pytest.status, result, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


# в функции валидации возраста больше нет нужды, так как появился отдельный тестовый набор негативных сценариев
@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                        ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                         russian_chars().upper(), chinese_chars()]
   , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials',
          'russian', 'RUSSIAN', 'chinese'])
@pytest.mark.parametrize("pet_photo", ['images/text.txt'], ids=['text.txt'])
def test_add_new_pet_negative(name, animal_type,
                           age, pet_photo):
    """ Отрицательные тесты с невалидными параметрами """
    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # добавляем питомца
    pytest.status, result, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 400
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type
