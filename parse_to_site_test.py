import requests #библиотека для работы с http запросами
from bs4 import BeautifulSoup #для работы с html страницами
import csv #модуль для работы с CSV

URL = 'https://kazandigital.ru/catalogue_category-category_id-47.html' #url сайта
URL1 = 'https://www.skynet-kazan.com/root/map'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'accept': '*/*'} # заголовки что бы сайт нас не заблокировал и считал за пользователя
HOST = 'https://kazandigital.ru/'
FILE = 'file.csv'

def get_html(url, params=None):
    '''
    :param url: url с которой необходимо получить контент
    :param params: опциональный аргумент (если будет несколько страниц - page, что бы передавать номера страниц)
    :return: возвр что вернет наш get запрос
    '''
    r = requests.get(url, headers=HEADERS, params=params) #делаем get запрос
    return r

def get_pages_coount(html):
    '''
    функуия которая возвращает количество строк
    :param html:
    :return:
    '''
    soup = BeautifulSoup(html, 'html.parser')
    #pagination = soup.find_all('span', class_='mhide') #возвращает все элементы класса mhide - все номера страниц
    #if pagination:
        #return int(pagination[-1].get_text()) #проверка на то что страниц больше одной - тут вернет последний элемент
    #else:
        #return 1 #вернет 1 если страниц - 1

def get_content(html):
    '''
    для работы с контентом страницы
    '''
    soup = BeautifulSoup(html, 'html.parser') #'html.parser' - тип документа с которым мы работаем
    items = soup.find_all('div', class_='item item_fixed1')  #тег 'div' с классом item....
    smartphones=[] #пустой список
    for item in items:
        smartphones.append({
            'title': item.find('div', class_='title').get_text(strip=True),
            'link': HOST + item.find('a',).get('href'),
            'price': item.find('div', class_='price_list_old').get_text(),
        }) #проходимся по каждому элементу и ищем объекты title и выбираем текст, добавляем в конец списка smaptphones
    print(smartphones)
    print(len(smartphones))

def save_files(items, path): #функция для сохранения файлов  принимает объект и путь куда надо сохранить
    with open(path, 'w', newline='') as file: #открывает файл по заданному пути, или создает его там если его там нет
        writer = csv.writer(file, delimiter=';') #используем writer для file
        writer.writerow(['Цена', 'Марка']) #запись в file и обозначение названий колонок
        for item in items:
            writer.writerow([item['title'], item['link'], item['price']]) #циклом проходимся по списку переданных объектов и записываем используя ключи

def parse():
    '''
    функция парсер
    '''
    html = get_html(URL) # вызываем функцию выше
    if html.status_code == 200: #если ответ от страницы 200, значит все ок
         cars = []
         get_content(html.text)
         pages_count = get_pages_coount(html.text)
         #for page in range(1, pages_count + 1): #цикл для прохода по всем страницам
             #print(f'Парсинг страницы {page} из {pages_count}...' ) #сообщение для пользователя
             #html = get_html(URL, params={'page': page}) #получаем контент для каждой страницы
             #cars.extend(get_content(html.text)) #парсим контент и расширяему его в список
        #save_files(cars, FILE) #передаем функции список с авто и путь до файла(в нашем случае файл созданный в той же папке)
    else:
        pass

parse() #вызов функции парсера