import telebot
import requests
#import config
from bs4 import BeautifulSoup
from pprint import pprint as pp



access_token = '483861578:AAG9dsrOaJWMGgTEBHYdFobITwxR4m1Zz2A'
bot = telebot.TeleBot(access_token)


if __name__ == '__main__':
    bot.polling(none_stop=True)


    def get_page(week = 1):
        f = open('web_page'+ str(week) +'.txt')
        web_page = f.read()
        f.close()
        return web_page


def get_schedule(web_page):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday'])
def get_monday(message):
    _, week = message.text.split()
    web_page = get_page(week)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page)

    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')
