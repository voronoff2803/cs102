import requests
from pprint import pprint as pp
import webbrowser
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import time
from igraph import Graph, plot


def get_access_token(client_id, scope):  # Получение токена доступа к сообщениям - get_access_token(6224304, 'messages')
    assert isinstance(client_id, int), 'clinet_id must be positive integer'
    assert isinstance(scope, str), 'scope must be string'
    assert client_id > 0, 'clinet_id must be positive integer'
    url = """\
    https://oauth.vk.com/authorize?client_id={client_id}&\
    redirect_uri=https://oauth.vk.com/blank.hmtl&\
    scope={scope}&\
    &response_type=token&\
    display=page\
    """.replace(" ", "").format(client_id=client_id, scope=scope)
    webbrowser.open_new_tab(url)
    print(url)

class JSONException(BaseException):
    pass


def get(query, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param query: тело GET запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for n in range(max_retries):
        try:
            response = requests.get(query, params=params, timeout=timeout)
            content_type = response.headers.get('Content-Type')
            if not content_type == "application/json; charset=utf-8":
                raise JSONException
            return response
        except requests.exceptions.RequestException:
            if n >= max_retries:
                raise
            backoff = backoff_factor * (2 ** n)
            time.sleep(backoff)


def get_age(bdate):
    if '.' not in bdate[len(bdate)-4:] and len(bdate) > 4:
        return bdate[len(bdate)-4:]


def get_friends(user_id, fields = "id"):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '605fdc99b8f9da9fe249c7e7dc288a74852efb15ccc24732b95bf2780affe69adec140c6f9b96a11c3085'
    user_id = user_id

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
        **query_params)
    try:
        print(query)
        response = get(query)
    except JSONException:
        return []
    try:
        resp = response.json()
        a = []
        for i in range(resp['response']['count']):
            try:
                if resp['response']['items'][i][fields]:
                    a.append(resp['response']['items'][i][fields])
            except:
                pass
        return a
    except:
        pass


def age_predict(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    if user_id:
        a = get_friends(user_id, 'bdate')
        ages = []
        for i in a:
            if '.' not in i[len(i) - 4:] and len(i) > 4 and get_age(i):
                ages.append(int(get_age(i)))
        max = ages[0] # max_age
        max_count = ages.count(max)
        for el in ages:
            if ages.count(el) > max_count:
                max = el
            max_count = ages.count(el)
        return (2017 - max)


def messages_get_history_json(user_id, offset=0, count=20):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '605fdc99b8f9da9fe249c7e7dc288a74852efb15ccc24732b95bf2780affe69adec140c6f9b96a11c3085'
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
    response = get(query)
    return response.json()


def messages_get_history(user_id, offset, need_count):


    plotly.tools.set_credentials_file(username='voronoff2803', api_key='8GDrahNhJyVMiiC5105i')  # Авторизация в pltly
    try:
        count = messages_get_history_json(user_id, 0, 1)['response']['count']
        if need_count < count:
            count = need_count
        dates = []
        for x in range((count - offset) // 200):
            time.sleep(1)
            messages = messages_get_history_json(user_id, offset + 200 * x, 200)
            print('скачанно: ', len(dates), '/', count - offset)
            for i in range(200):
                dates.append(messages['response']['items'][i]['date'])
        messages = messages_get_history_json(user_id, offset + 200 * (count // 200), count % 200)
        for i in range(count % 200 - 1):
            dates.append(messages['response']['items'][i]['date'])
        print('скачанно: ', len(dates) + 1, '/', count - offset)
        return (dates)
    except:
        pp(messages_get_history_json(user_id, 0, 1))


def message_plotly(users_ids):

    def count_dates_from_dates(messages):
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

    dates = messages_get_history(144792435, 0, 300)
    list = count_dates_from_dates(dates)
    data = [go.Scatter(x=list[0], y=list[1])]
    py.plot(data)


def get_friends_graph(user_id, fields = "id", iscount = False):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '605fdc99b8f9da9fe249c7e7dc288a74852efb15ccc24732b95bf2780affe69adec140c6f9b96a11c3085'
    user_id = user_id

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
        **query_params)
    response = get(query)
    resp = response.json()
    if iscount:
        return resp['response']['count']
    a = []
    for i in range(resp['response']['count']):
        try:
            if resp['response']['items'][i][fields]:
                a.append(resp['response']['items'][i][fields])
        except:
            pass
    return a


friends_pop = []


def get_network(users_ids, as_edgelist=True):
    edges = []
    for x, x_id in enumerate(users_ids):
        try:
            friends_ids_x = get_friends(x_id)
            if len(friends_ids_x) < 600:
                friends_pop.append(6 + len(friends_ids_x) * 0.03)
            else:
                friends_pop.append(6 + 600 * 0.03)
            print('Прогресс: ' + str(x + 1) + '/' + str(len(users_ids)))
            time.sleep(0.2)
            for y, y_id in enumerate(users_ids):
                if y_id in friends_ids_x:
                    edges.append((x, y))
        except:
            pass
    return(edges)


def drow_graph(id_for_graph):
    friends_lastnames = get_friends(id_for_graph, 'last_name')
    friends_sex = get_friends(id_for_graph, 'sex')

    myedges = get_network(get_friends(id_for_graph), as_edgelist=True)

    vertices = friends_lastnames
    edges = myedges

    g = Graph(vertex_attrs={"label": vertices, "gender": friends_sex, "pop": friends_pop},
              edges=edges, directed=False)
    g.simplify(multiple=True, loops=True)

    N = len(vertices)
    color_dict = {2 : "light sky blue", 1 : "pink"}
    visual_style = {}
    visual_style["vertex_size"] = 8
    visual_style["vertex_label"] = g.vs["label"]
    visual_style["bbox"] = (1000, 1000)
    visual_style["margin"] = 100
    visual_style["vertex_label_dist"] = 1.6
    visual_style["vertex_label_color"] = "black"
    visual_style["edge_color"] = "gray"
    visual_style["autocurve"] = True
    g.vs["color"] = [color_dict[gender] for gender in g.vs["gender"]]
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=100000,
        area=N ** 2,
        repulserad=N ** 2)

    plot(g,str(id_for_graph)+".png", **visual_style)

#get_access_token(6224304, 'messages')
print(age_predict(409402304))  # Функция предсказывает возраст по id
#message_plotly(144792435)  # Функция строит график переписки с человеком (если возращает ошибку - значит график построен(баг модуля plotly))
#drow_graph(210922771)  # Строит граф друзей
