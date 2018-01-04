import requests
import re
from bs4 import BeautifulSoup
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bottle import route, run, template, request, redirect


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)


def save_database(dict):
    s = session()
    for current_new in dict:
        news = News(title=current_new['title'],
                    author=current_new['author'],
                    url=current_new['url'],
                    points=current_new['points'])
        s.add(news)
    s.commit()

def get_page(url):
    try:
        response = requests.get(url)
        if response.ok:
            return response.text
        else:
            print("Error " + str(response.status_code))
            return False
    except requests.exceptions.ConnectTimeout:
        print('Oops. Connection timeout occured!')
    except requests.exceptions.ReadTimeout:
        print('Oops. Read timeout occured')
    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed..')


def get_news(url, n_pages):
    def extract_news(url):
        response = get_page(url)
        page = BeautifulSoup(response, 'html5lib')
        tr = page.body.center.table.findAll('tr')[3]
        hnusers = tr.td.table.tbody.findAll('a', {'class': 'hnuser'})
        scores = tr.td.table.tbody.findAll('span', {'class': 'score'})
        titles = tr.td.table.tbody.findAll('a', {'class': 'storylink'})
        dict = []
        for i in range(len(hnusers)):
            dict.append({'author': hnusers[i].text,
                         'points': int(re.findall('(\d+)', scores[i].text)[0]),
                         'title': titles[i].text,
                         'url': titles[i].get('href')
                         })
        return dict

    all_dict = []
    for current_page in range(n_pages):
        all_dict += extract_news(url)
        response = get_page(url)
        page = BeautifulSoup(response, 'html5lib')
        newurl = page.find('a', {'class': 'morelink'})
        url = 'https://news.ycombinator.com/' + newurl.get('href')
    return all_dict


@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route('/add_label/')
def add_label(label="maybe",id=1):
    label = request.query.label
    id = request.query.id
    s = session()
    items = s.query(News).filter(News.id == id).all()
    print(items)
    for item in items:
        item.label = label
    s.commit()
    redirect('/news')


@route('/update_news')
def update_news():
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    dicts = get_news('https://news.ycombinator.com/newest', 1)
    bd_labels = []
    for row in rows:
        bd_labels.append(row.title)
    for current_new in dicts:
        if current_new['title'] not in bd_labels:
            news = News(title=current_new['title'],
                        author=current_new['author'],
                        url=current_new['url'],
                        points=current_new['points'])
            s.add(news)
    s.commit()

    redirect('/news')
#dicts = get_news('https://news.ycombinator.com/newest', 2)
#save_database(dicts)

run(host='localhost', port=8080)