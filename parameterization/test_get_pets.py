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
@pytest.mark.parametrize("filter_",
                        [
                            generate_string(255)
                            , generate_string(1001)
                            , russian_chars()
                            , russian_chars().upper()
                            , chinese_chars()
                            , special_chars()
                            , 123
                        ],
                        ids =
                        [
                            '255 symbols'
                            , 'more than 1000 symbols'
                            , 'russian'
                            , 'RUSSIAN'
                            , 'chinese'
                            , 'specials'
                            , 'digit'
                        ])
def test_get_all_pets_with_negative_filter(filter_):
    """Негативные тесты на получение списка питомцев с различными параметрами пути"""
    status, result, res = pf.get_list_of_pets(auth_key, filter_)
    # сервер корректно обрабатывает запросы и возвращает 400 код
    assert status == 400
    return res


@pytest.mark.parametrize("filter_",
                        ['', 'my_pets'],
                        ids=['empty string', 'only my pets'])
def test_get_all_pets_with_positive_filter(filter_):
    """Позитивные тесты на получение списка питомцев с различными параметрами пути """
    status, result, res = pf.get_list_of_pets(auth_key, filter_)
    assert status == 200
    assert len(result['pets']) > 0
    return res
