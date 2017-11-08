import requests
from pprint import pprint as pp
import webbrowser
import argparse


def get_access_token(client_id, scope):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="Application Id", type=int)
    parser.add_argument("-s",
                        dest="scope",
                        help="Permissions bit mask",
                        type=str,
                        default="",
                        required=False)
    args = parser.parse_args()
    get_access_token(args.client_id, args.scope)


access_token = get_access_token(199785621, "messages")
print(access_token)

def GetAge(bdate):
    if '.' not in bdate[len(bdate)-4:] and len(bdate) > 4:
        return bdate[len(bdate)-4:]


def get_friends(user_id, fields = "id"):
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
    access_token = 'a5c77183a5c77183a5c771831fa5998833aa5c7a5c77183fc211e505179f0d569aa23b5'
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




print(age_predict(57899071))
history = messages_get_history(394481525, 0, 3)
pp(history)