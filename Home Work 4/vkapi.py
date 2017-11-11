import requests
from pprint import pprint as pp
import webbrowser
import argparse


def GetAge(bdate):
    if '.' not in bdate[len(bdate)-4:] and len(bdate) > 4:
        return bdate[len(bdate)-4:]


def get_friends(user_id, fields = "id"):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '70ee2e1ff976d05511ef99d959a8be668e44b8ec314a18cf87ed6067012572e7d3046e094a87615ebf0b8'
    user_id = user_id

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
        **query_params)
    response = requests.get(query)
    resp = response.json()
    a = []
    for i in range(resp['response']['count']):
        try:
            if resp['response']['items'][i][fields]:
                a.append(resp['response']['items'][i][fields])
        except:
            pass
    return a


def age_predict(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    if user_id:
        sum = 0
        count = 0
        a = get_friends(user_id, 'bdate')
        ages = []
        for i in a:
            if '.' not in i[len(i) - 4:] and len(i) > 4 and GetAge(i):
                ages.append(int(GetAge(i)))
        max = ages[0]
        max_count = ages.count(max)
        for el in ages:
            if ages.count(el) > max_count:
                max = el
            max_count = ages.count(el)
        return (2017 - max)


def messages_get_history(user_id, offset=0, count=20):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '70ee2e1ff976d05511ef99d959a8be668e44b8ec314a18cf87ed6067012572e7d3046e094a87615ebf0b8'
    user_id = user_id

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'offset': offset,
        'count': count
    }

    query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v=5.53".format(
        **query_params)
    response = requests.get(query)
    return response.json()



print(age_predict(138091639))
history = messages_get_history(394481525, 0, 3)
pp(history)