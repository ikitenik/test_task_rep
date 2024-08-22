import requests


def answer(response):
    if response.status_code == 200:
        print('Success:', response.json())
    else:
        print('Failed:', response.status_code, response.text)


def get(url_get, pk=None):
    if pk:
        response_get = requests.get(url_get + f'{pk}/')
        answer(response_get)
        return
    response_get = requests.get(url_get)
    answer(response_get)


def put(url_put, pk, data_put):
    response_put = requests.put(url_put + f'{pk}/', json=data_put)
    answer(response_put)


def post(url_post, data_put):
    response_post = requests.post(url_post, json=data_put)
    answer(response_post)


def delete(url_delete, pk=None):
    response_delete = requests.delete(url_delete + f'{pk}/')
    answer(response_delete)


url = 'http://localhost:8000/api/materials/'  # Полный адрес эндпоинта
url_type = 'http://localhost:8000/api/material_types/'
url_tree = 'http://localhost:8000/api/categories/'
data = {
    'type': 26,
    'material_name': 'BeforeTes1t2',
    'material_price': 1000
}
data_type = {
    'category': 2,
    'type_name': 'AfterTest'
}

#get(url_type, 2)
#delete(url, 37)
#put(url, 1, data)
#post(url_type, data_type)
#get(url_type)
get(url_tree)
