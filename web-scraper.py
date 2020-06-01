from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import time
import os

def access_page(url):
    try:
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")
        base_url = urlparse(url)
        save_page(base_url.netloc, base_url.path, data)
        for link in soup.find_all('a'):
            new_url = link.get('href')
            parsed_url = urlparse(new_url)
            if parsed_url.scheme:
                queue_push(link.get('href'))
                save_reference(parsed_url.netloc, parsed_url.path, base_url.netloc + base_url.path)

    except requests.exceptions.RequestException as err:
        print('The provided url is invalid: ' + url)
        print(err)

def is_page_visited(url):
    parsed_url = urlparse(url)
    filepath = './pages' + parsed_url.netloc + parsed_url.path + '/index.html'
    if os.path.exists(os.path.dirname(filepath)):
        return True
    else:
        return False

def save_page(url, path, pagedata):
    filepath = './pages/' + url + path + '/index.html'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc:
            print(exc)
    with open(filepath, 'w') as f:
        f.write(pagedata)

def read_from_queue(line_num):
    with open("./queue.txt") as queue:
        for i, line in enumerate(queue):
            if i == line_num - 1:
                return line

def save_reference(url, path, reference_url):
    filepath = './pages/' + url + path + '/reference'
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc:
            print(exc)
    try:
        with open(filepath, 'a+') as f:
            if not reference_url in f.read():
                f.write(reference_url.strip("\n\r ") + os.linesep)
    except OSError as err:
        print(err)

def queue_init(url):
    with open('./queue.txt', 'w+') as queue:
        queue.write(url)

def queue_push(url):
    with open("./queue.txt", "a+") as queue:
        queue.write("\n" + url)

def init():
    queue_init('https://github.com/')
    line_num = 1
    processed_num = 1
    url = read_from_queue(line_num)
    while url:
        print(url, processed_num)
        if not is_page_visited(url):
            access_page(url)
            processed_num += 1
        line_num += 1
        url = read_from_queue(line_num)
        time.sleep(1)

init()