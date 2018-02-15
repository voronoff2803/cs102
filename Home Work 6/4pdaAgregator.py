import requests
import pprint
from bs4 import BeautifulSoup
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bottle import route, run, template, request, redirect
import bayes


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    text = Column(String)
    author = Column(String)
    url = Column(String)
    img = Column(String)
    comments = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)


def save_database(dicts):
    s = session()
    rows = s.query(News).filter().all()
    bd_labels = []
    for row in rows:
        bd_labels.append(row.title)
    print(bd_labels)
    for current_new in dicts:
        if current_new['title'] not in bd_labels:
            news = News(title=current_new['title'],
                        text=current_new['text'],
                        author=current_new['author'],
                        url=current_new['url'],
                        img = current_new['img'],
                        comments=current_new['comments'])
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
        posts = page.find_all('article', {'class': 'post'})
        postsdict = []
        for post in set(posts):
            title = post.find_next('span', {'itemprop': 'name'})
            text = post.find_next('p', {'style': 'text-align: justify;'})
            author = post.find_next('span', {'class': 'autor'})
            url = post.find_next('a', {'class': 'btn-more'})
            comments = post.find_next('a', {'class': 'v-count'})
            img = post.find_next('img', {'itemprop': 'image'})
            try:
                postsdict.append({'title': title.text,
                                  'text': text.text,
                                  'author': author.text,
                                  'url': url['href'],
                                  'img': img['src'],
                                  'comments': comments.text
                                 })
            except:
                pass
        return postsdict

    postsdict = []
    for current_page in range(n_pages):
        postsdict += extract_news(url + str(current_page + 1))

    return postsdict


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
    dicts = get_news('http://4pda.ru/page/', 3)
    save_database(dicts)
    redirect('/news')


@route('/')
def goto_news():
    redirect('/news')


@route('/recommendations')
def recommendations():
    s = session()
    classified_news = s.query(News).filter(News.label == 'good').all()
    return template('news_template2', rows=classified_news)

@route('/getrecommendations')
def get_recommendations():
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    x = []
    y = []
    for row in rows:
        x.append(row.title)
        y.append(row.label)
    bayesclassifier = bayes.NaiveBayesClassifier()
    bayesclassifier.fit(x, y)
    s.commit()
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    for row in rows:
        try:
            row.label = bayesclassifier.predict(row.title)
        except:
            pass
    s.commit()
    redirect('/recommendations')
run(host='localhost', port=8080)