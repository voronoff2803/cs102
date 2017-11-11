import requests
from pprint import pprint as pp
import webbrowser
import argparse
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import time

plotly.tools.set_credentials_file(username='voronoff2803', api_key='2CqqTTtIebNiQ2U61Wnx')


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


def count_dates_from_dates(messages): # Функция для сбора статистики с более 200 сообщений
    dates = []
    numbers = []
    count = 1
    for i in range(len(messages)-1):
        if (datetime.fromtimestamp(messages[i]).strftime("%Y-%m-%d") ==
                datetime.fromtimestamp(messages[i + 1]).strftime("%Y-%m-%d")):
            count += 1
        else:
            dates.append (datetime.fromtimestamp(messages[i]).strftime("%Y-%m-%d"))
            numbers.append(count)
            count = 1
    return dates, numbers


def get_many_dates(user_id, offset):
    count = messages_get_history(user_id, 0, 1)['response']['count']
    dates = []
    for x in range((count - offset) // 200):
        print('скачанно: ',x*200,'/',count)
        time.sleep(2)
        messages = messages_get_history(user_id, offset + 200 * x, 200)
        for i in range(200):
            dates.append(messages['response']['items'][i]['date'])
    return (dates)


dates = get_many_dates(144792435, 0)

list = count_dates_from_dates(dates)
#pp (len(dates))
data = [go.Scatter(x=list[0],y=list[1])]
py.iplot(data)