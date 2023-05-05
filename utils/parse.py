#!/usr/bin/python
# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup


def kyiv():
    links = []
    titles = []
    messages = []
    url = 'https://kyivcity.gov.ua'
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    temp = bs.find('ul', 'mainBoard__list').find_all('a', 'previewOnTab__left')
    for i in temp:
        titles.append(i['title'])
        links.append(i['href'])
    for i, title in enumerate(titles):
        try:
            message = ''
            link = links[i]
            page = BeautifulSoup(requests.get(url + link).text, 'html.parser')
            date = page.find('div', 'news__inner-date pull-left').text
            content = page.find('div', 'row fullpage fullpage__inner').find('div', 'col-md-12')
            for j in content:
                try:
                    text = ''
                    if j.name == 'ul':
                        for li in j:
                            li = BeautifulSoup(str(li), 'html.parser').text
                            text += li + '\n' if li != ' ' else li
                    else:
                        text = j.text if j.text != ' ' else ''
                    message += text + '\n'
                except:
                    pass
            message = title + '\n\n' + message.rstrip().lstrip() + '\n\n' + date
            messages.append(message)
        except:
            continue
    return messages


def lviv():
    links = []
    messages = []
    url = 'https://www.032.ua/news'
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    temp = bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-block__title')
    temp.extend(bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-card__title'))
    for i in temp:
        title = i.text
        title = title.replace(', - ФОТО', '')
        title = title.replace(', - ВІДЕО', '')
        links.append((title, i['href']))
    for title, link in links:
        try:
            page = BeautifulSoup(requests.get(link).text, 'html.parser')
            content = page.find('div', 'article-details__text').find_all('p')
            date = page.find('div', 'article-details__date').text
            text = []
            for i in content:
                i = BeautifulSoup(str(i), 'html.parser')
                text.append(i.text)
            message = title + '\n'
            for i in text:
                message += '\n' + i
            message = message.rstrip() + '\n\n' + date
            messages.append(message)
        except:
            continue
    return messages


def kharkiv():
    links = []
    messages = []
    url = 'https://www.057.ua/news'
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    temp = bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-block__title')
    temp.extend(bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-card__title'))
    for i in temp:
        title = i.text
        title = title.replace(', - ФОТО', '')
        title = title.replace(', - ВІДЕО', '')
        links.append((title, i['href']))
    for title, link in links:
        try:
            page = BeautifulSoup(requests.get(link).text, 'html.parser')
            content = page.find('div', 'article-details__text').find_all('p')
            date = page.find('div', 'article-details__date').text
            text = []
            for i in content:
                i = BeautifulSoup(str(i), 'html.parser')
                text.append(i.text)
            message = title + '\n'
            for i in text:
                message += '\n' + i
            message = message.rstrip() + '\n\n' + date
            messages.append(message)
        except:
            continue
    return messages


def vinnytsia():
    links = []
    messages = []
    url = 'https://www.0432.ua/news'
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    temp = bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-block__title')
    temp.extend(bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-card__title'))
    for i in temp:
        title = i.text
        title = title.replace(', - ФОТО', '')
        title = title.replace(', - ВІДЕО', '')
        links.append((title, i['href']))
    for title, link in links:
        try:
            page = BeautifulSoup(requests.get(link).text, 'html.parser')
            content = page.find('div', 'article-details__text').find_all('p')
            date = page.find('div', 'article-details__date').text
            text = []
            for i in content:
                i = BeautifulSoup(str(i), 'html.parser')
                text.append(i.text)
            message = title + '\n'
            for i in text:
                message += '\n' + i
            message = message.rstrip() + '\n\n' + date
            messages.append(message)
        except:
            continue
    return messages


def dnipro():
    links = []
    messages = []
    url = 'https://www.056.ua/news'
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    temp = bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-block__title')
    temp.extend(bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-card__title'))
    for i in temp:
        title = i.text
        title = title.replace(', - ФОТО', '')
        title = title.replace(', - ВІДЕО', '')
        links.append((title, i['href']))
    for title, link in links:
        try:
            page = BeautifulSoup(requests.get(link).text, 'html.parser')
            content = page.find('div', 'article-details__text').find_all('p')
            date = page.find('div', 'article-details__date').text
            text = []
            for i in content:
                i = BeautifulSoup(str(i), 'html.parser')
                text.append(i.text)
            message = title + '\n'
            for i in text:
                message += '\n' + i
            message = message.rstrip() + '\n\n' + date
            messages.append(message)
        except:
            continue
    return messages


def odesa():
    links = []
    messages = []
    url = 'https://www.048.ua/news'
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    temp = bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-block__title')
    temp.extend(bs.find('div', 'col-12 col-md-8 col-lg-9').find_all('a', 'c-news-card__title'))
    for i in temp:
        title = i.text
        title = title.replace(', - ФОТО', '')
        title = title.replace(', - ВІДЕО', '')
        title = title.replace(', ФОТО', '')
        title = title.replace(', ВІДЕО', '')
        links.append((title, i['href']))
    for title, link in links:
        try:
            page = BeautifulSoup(requests.get(link).text, 'html.parser')
            content = page.find('div', 'article-details__text').find_all('p')
            date = page.find('div', 'article-details__date').text
            text = []
            for i in content:
                i = BeautifulSoup(str(i), 'html.parser')
                text.append(i.text)
            message = title + '\n'
            for i in text:
                message += '\n' + i
            message = message.rstrip() + '\n\n' + date
            messages.append(message)
        except:
            continue
    return messages


func_list = [(name, obj) for name, obj in vars().items()
                 if hasattr(obj, "__class__") and obj.__class__.__name__ == "function"]
