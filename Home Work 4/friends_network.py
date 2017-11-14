from igraph import Graph, plot
import numpy as np
import requests
from pprint import pprint as pp
import time


def get_friends(user_id, fields = "id", iscount = False):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = 'a5c77183a5c77183a5c771831fa5998833aa5c7a5c77183fc211e505179f0d569aa23b5'
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


def get_network(users_ids, as_edgelist=True):
    edges = []
    for x, x_id in enumerate(users_ids):
        try:
            friends_ids_x = get_friends(x_id)
            print('Прогресс: ' + str(x + 1) + '/' + str(len(users_ids)))
            time.sleep(0.5)
            for y, y_id in enumerate(users_ids):
                if y_id in friends_ids_x:
                    edges.append((x, y))
        except:
            pass
    return(edges)

def drow_graph(id_for_graph):
    friends_ids = get_friends(id_for_graph, 'id')
    friends_firstnames = get_friends(id_for_graph, 'first_name')
    friends_lastnames = get_friends(id_for_graph, 'last_name')

    myedges = get_network(get_friends(id_for_graph), as_edgelist=True)

    vertices = get_friends(id_for_graph, 'last_name')
    edges = myedges

    g = Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)
    g.simplify(multiple=True, loops=True)

    N = len(vertices)
    visual_style = {}
    visual_style["vertex_size"] = 8
    visual_style["vertex_label"] = g.vs["label"]
    visual_style["bbox"] = (1000, 1000)
    visual_style["margin"] = 100
    visual_style["vertex_label_dist"] = 2
    visual_style["vertex_color"] = "gray"
    visual_style["vertex_label_color"] = "black"
    visual_style["edge_color"] = "gray"
    visual_style["autocurve"] = True
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=100000,
        area=N ** 2,
        repulserad=N ** 2)
    plot(g, **visual_style)

drow_graph(394481525)