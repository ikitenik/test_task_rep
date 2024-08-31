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


url_mat = 'http://localhost:8000/api/materials/'
data_mat = {
    'category': 5,
    'name': "Дверь вроде бы",
    'price': 3000,
}

url_cat = 'http://localhost:8000/api/categories/'
data_cat = {
     "name": "Воздушные фильтры",
     "parent": 9,
     "children": None
}

url_cat_list = 'http://localhost:8000/api/flat/'
#post(url_cat, data_cat)
#post(url_mat, data_mat)
get(url_cat_list)
#put(url, 2, data)
#post(url_cat, data_cat)
#post(url_mat, data_mat)
#get(url_type)

