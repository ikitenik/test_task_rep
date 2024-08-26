import requests


def answer(response):
    if response.status_code == 200 or response.status_code == 201:
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


url_mat = 'http://localhost:8000/api/materials/'  # Полный адрес эндпоинта
url_type = 'http://localhost:8000/api/material_types/'
url_cat = 'http://localhost:8000/api/categories/list/'

data_mat = {
    'type': 2,
    'material_name': "Дверь задняя Toyota Ractis",
    'material_price': -3333,
}

data_type = {

}

data_cat = {
    'category_name': "Test_cat"
}

#post(url, data)
#put(url, 2, data)
#post(url_cat, data_cat)
#get(url_cat)
#delete(url_cat, 6)
#put(url_cat, 5, data_cat)
get(url_cat)
#delete(url, 37)
#put(url, 1, data)
#post(url_type, data_type)
#get(url_type)
#get(url_tree)
