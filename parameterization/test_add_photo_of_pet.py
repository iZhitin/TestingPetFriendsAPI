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

@pytest.mark.parametrize("pet_photo", ['images/P1040103.jpg', 'images/1.bmp', 'images/1px.jpg', 'images/10kX10k.jpg', 'images/cat1.gif', 'images/cat1.png'], ids=['image.jpg', 'image.bmp', '1px', '10kX10k', 'image.gif', 'image.png'])
def test_successful_add_photo(pet_photo):
    """Позитивные кейсы добавления фото"""
    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # получаем ключ auth_key и список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")
    # если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result, res = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        return res
    else:
        # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

@pytest.mark.parametrize("pet_photo", ['images/text.txt'], ids=['text.txt'])
def test_unsuccessful_add_photo(pet_photo):
    """Негативные кейсы добавления фото"""
    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # получаем ключ auth_key и список своих питомцев
    _, my_pets, _ = pf.get_list_of_pets(auth_key, "my_pets")
    # если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result, res = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        return res
    else:
        # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
