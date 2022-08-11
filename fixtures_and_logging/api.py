# для работы с объектами json
import json

# для работы с HTTP запросами
import requests

# для отправки фото через API
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """API-библиотека к веб-приложению PetFriends"""

    # инициализация базового URL
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролю"""

        # формирование заголовков в виде словаря
        headers = {
            'email': email,
            'password': passwd,
        }
        # отправка запроса get и получение ответа
        res = requests.get(self.base_url + 'api/key', headers=headers)
        # cтатус запроса
        status = res.status_code
        # попытаемся преобразовать ответ в json, если нет - в текст
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        # функция выводит статус запроса, содержимое ответа и сам ответ
        return status, result, res

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        # формирование заголовков в виде словаря с ключом авторизации
        headers = {'auth_key': auth_key['key']}
        # формирование параметров пути в виде словаря с фильтром
        filter = {'filter': filter}

        # отправка запроса get и получение ответа
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        # статус запроса
        status = res.status_code
        # попытаемся преобразовать ответ в json, если нет - в текст
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        # функция выводит статус запроса, содержимое ответа и сам ответ
        return status, result, res

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        # формирование тела запроса
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        # формирование заголовков в виде словаря с ключом авторизации и типом содержимого
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        # отправка запроса post и получение ответа
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        # статус запроса
        status = res.status_code
        # попытаемся преобразовать ответ в json, если нет - в текст
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        # функция выводит статус запроса, содержимое ответа и сам ответ
        return status, result, res

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления об успешном удалении"""

        # формирование заголовков в виде словаря с ключом авторизации
        headers = {'auth_key': auth_key['key']}

        # отправка запроса delete и получение ответа
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        # статус запроса
        status = res.status_code
        # попытаемся преобразовать ответ в json, если нет - в текст
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        # функция выводит статус запроса, содержимое ответа и сам ответ
        return status, result, res

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и
        возвращает статус запроса и результат в формате JSON с обновленными данными питомца"""

        # формирование заголовков в виде словаря с ключом авторизации
        headers = {'auth_key': auth_key['key']}
        # формирование тела запроса
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        # отправка запроса put и получение ответа
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        # статус запроса
        status = res.status_code
        # попытаемся преобразовать ответ в json, если нет - в текст
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        # функция выводит статус запроса, содержимое ответа и сам ответ
        return status, result, res

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет (постит) на сервер данные БЕЗ ФОТО о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        # формирование заголовков в виде словаря с ключом авторизации
        headers = {'auth_key': auth_key['key']}
        # формирование тела запроса
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        # отправка запроса post и получение ответа
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        # статус запроса
        status = res.status_code
        # попытаемся преобразовать ответ в json, если нет - в текст
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        # функция выводит статус запроса, содержимое ответа и сам ответ
        return status, result, res

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер ФОТО питомца по его ID и возвращает статус
        запроса на сервер и результат в формате JSON с данными питомца. Данную операцию
        можно провести только через API"""

        # формирование тела запроса
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        # формирование заголовков в виде словаря с ключом авторизации и типом содержимого
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        # отправка запроса post и получение ответа
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        # статус запроса
        status = res.status_code
        # попытаемся преобразовать ответ в json, если нет - в текст
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        # print(result)
        # функция выводит статус запроса, содержимое ответа и сам ответ
        return status, result, res
