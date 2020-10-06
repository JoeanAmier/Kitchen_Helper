import time
import random
import sqlite3
from requests_html import HTMLSession


def keyword():
    key = input('搜索关键字：')
    # 生成搜索链接
    url = 'http://www.xiachufang.com/search/?keyword={}&cat=1001'.format(key)
    return key, url  # 返回关键字和搜索链接


def get_url(url):
    """获取每个菜品的详细链接"""
    item_url = []
    html = open_url(url)  # 请求链接
    time.sleep(random.randrange(4, 7, 1))  # 减慢爬取速度
    href = html.html.find(
        '.recipe.recipe-215-horizontal.pure-g.image-link.display-block > a')  # 匹配每个菜品的详细链接
    for url in href[:3]:  # 只获取前 10 个菜品的详细链接，可修改
        item_url.append('http://www.xiachufang.com' + url.attrs['href'])
    return item_url  # 返回搜索结果前 10 个菜品的详细链接


def open_url(url):
    session = HTMLSession()
    response = session.get(url)  # 向网站发送请求
    return response  # 返回网站响应


def get_data(url_list):
    data = []
    for item in url_list:  # 遍历前 10 个菜品的详细链接
        cache = []
        html = open_url(item)
        if str(html) == '<Response [200]>':
            time.sleep(random.randrange(4, 7, 1))  # 减慢爬取速度
            title = html.html.find('.page-title')
            if bool(title):
                cache.append(title[0].text)
            else:
                print(item)
                cache.append('')
            recipeIngredient = html.html.find('.ings')
            if bool(recipeIngredient):
                cache.append(recipeIngredient[0].text)
            else:
                print(item)
                cache.append('')
            recipeInstructions = html.html.find('.steps p.text')
            if bool(recipeInstructions):
                steps = ''
                for i in range(len(recipeInstructions)):
                    steps += recipeInstructions[i].text
                cache.append(steps)
            else:
                print(item)
                cache.append('')
            image = html.html.find(
                'div.cover.image.expandable.block-negative-margin > img')
            if bool(image):
                cache.append(image[0].attrs['src'])
            else:
                print(item)
                cache.append('')
            url = html.html.find('link[rel=canonical]')
            if bool(url):
                cache.append(url[0].attrs['href'])
            else:
                print(item)
                cache.append('')
            data.append(cache)
        else:
            break
    return data


def select_data(key):
    sqlite = sqlite3.connect('本周最受欢迎.db')
    cursor = sqlite.cursor()
    """SQL 语句，在菜名和用料查找并返回包含关键字的数据"""
    sql = '''select * from 本周最受欢迎
        where 菜名 like "%{}%" or 用料 like "%{}%"'''.format(key, key)
    result = cursor.execute(sql)  # 接收查询结果
    data = []
    for item in result:  # 遍历查询结果并提取数据
        data.append(item)
    if len(data) != 0:  # 判断是否有符合条件的数据
        return data  # 如果有符合要求的数据，返回数据
    else:
        return None  # 如果没有符合要求的数据，返回None，传递给后续函数，进行实时获取数据


def select(key):
    if bool(key):
        url = 'http://www.xiachufang.com/search/?keyword={}&cat=1001'.format(
            key)
        data = select_data(key)  # 在数据库查找菜名或用料包含关键字的数据
        if bool(data):  # 如果在数据库查找到数据，则输入返回的数据
            return '数据库', data  # 数据可视化使用
        else:  # 如果返回的数据为空，则实时查询
            url_list = get_url(url)
            data = get_data(url_list)
            if bool(data):
                return '实时获取', data  # 数据可视化使用
            else:
                return '实时获取', None
    else:
        return '无数据', None


def main():
    key, url = keyword()  # 输入关键字并生成搜索网址
    data = select_data(key)  # 在数据库查找菜名或用料包含关键字的数据
    if bool(data):  # 如果在数据库查找到数据，则输入返回的数据
        print(data)  # 数据可视化使用
        print('来自数据库')
    else:  # 如果返回的数据为空，则实时查询
        url_list = get_url(url)
        data = get_data(url_list)
        print(data)  # 数据可视化使用
        print('来自实时数据')


if __name__ == '__main__':
    main()
