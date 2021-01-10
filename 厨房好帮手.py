import time
import random
import sqlite3
from requests_html import HTMLSession
from 数据库更新 import all_data
import emoji
import re


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
    for url in href[:3]:  # 只获取前 3 个菜品的详细链接，可修改
        item_url.append('http://www.xiachufang.com' + url.attrs['href'])
    return item_url  # 返回搜索结果前 3 个菜品的详细链接


def open_url(url):
    session = HTMLSession()
    response = session.get(url)  # 向网站发送请求
    return response  # 返回网站响应


def get_data(url_list):
    data = []  # 储存总数据
    save = []
    for item in url_list:  # 遍历每一个菜品的详细链接
        cache = []  # 储存每个菜品的数据
        save_cache = []
        html = open_url(item)  # 发送请求
        if str(html) == '<Response [200]>':  # 判断是否请求成功
            time.sleep(random.randrange(4, 7, 1))  # 减慢爬取速度
            title = html.html.find('.page-title')  # 匹配菜名
            if bool(title):  # 判断匹配结果
                cache.append(title[0].text)  # 添加有效数据
                title = emoji.demojize(title[0].text)
                save_cache.append(title)
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
                save_cache.append('')  # 添加空数据，避免直接报错
            recipeIngredient = html.html.find('.ings')  # 匹配用料
            if bool(recipeIngredient):  # 判断匹配结果
                cache.append(recipeIngredient[0].text)  # 添加有效数据
                recipeIngredient = emoji.demojize(recipeIngredient[0].text)
                save_cache.append(recipeIngredient)
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
                save_cache.append('')  # 添加空数据，避免直接报错
            recipeInstructions = html.html.find('.steps p.text')  # 匹配做法步骤
            if bool(recipeInstructions):  # 判断匹配结果
                """这里匹配的结果是包含多项的列表，要先处理成单个字符串再添加有效数据"""
                steps = ''
                for i in range(len(recipeInstructions)):
                    """遍历匹配结果，这个数据是做法步骤，不同菜品的步骤数不相等，通过遍历组成单个字符串"""
                    steps += recipeInstructions[i].text
                cache.append(steps)  # 添加有效数据
                save_cache.append(emoji.demojize(steps))
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
                save_cache.append('')  # 添加空数据，避免直接报错
            image = html.html.find(
                'div.cover.image.expandable.block-negative-margin > img')  # 匹配效果图链接
            if bool(image):  # 判断匹配结果
                cache.append(image[0].attrs['src'])  # 添加有效数据
                save_cache.append(image[0].attrs['src'])  # 添加有效数据
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
                save_cache.append('')  # 添加空数据，避免直接报错
            url = html.html.find('link[rel=canonical]')  # 匹配详细链接
            if bool(url):  # 判断匹配结果
                cache.append(url[0].attrs['href'])  # 添加有效数据
                save_cache.append(url[0].attrs['href'])  # 添加有效数据
                find = re.compile(
                    r'https://www.xiachufang.com/recipe/([0-9]+?)/')
                id = re.findall(find, url[0].attrs['href'])
                if id:
                    cache.append(id[0])
                    save_cache.append(id[0])
                else:
                    print(url)
                    cache.append('')
                    save_cache.append('')
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
                save_cache.append('')  # 添加空数据，避免直接报错
            data.append(cache)  # 添加一个菜品的数据到总数据
            save.append(save_cache)  # 添加一个菜品的数据到总数据
        else:
            break  # 请求失败说明被封IP，跳出循环，爬取结束
    for i, j in enumerate(save):
        for index in range(len(j)):
            save[i][index] = '"' + save[i][index] + '"'
    all_data(save)
    return data  # 返回总数据的列表


def select_data(key):
    sqlite = sqlite3.connect('菜品数据库.db')
    cursor = sqlite.cursor()
    """SQL 语句，在菜名和用料查找并返回包含关键字的数据"""
    sql = '''select * from 本周最受欢迎
        where 菜名 like "%{}%" or 用料 like "%{}%"'''.format(key, key)
    result = cursor.execute(sql)  # 接收查询结果
    data = []
    for item in result:  # 遍历查询结果并提取数据
        item = list(item)
        item[0] = emoji.emojize(item[0])
        item[1] = emoji.emojize(item[1])
        item[2] = emoji.emojize(item[2])
        data.append(item)
    if len(data) != 0:  # 判断是否有符合条件的数据
        return data  # 如果有符合要求的数据，返回数据
    else:
        return None  # 如果没有符合要求的数据，返回None，传递给后续函数，进行实时获取数据


def select_all_data(key):
    sqlite = sqlite3.connect('菜品数据库.db')
    cursor = sqlite.cursor()
    """SQL 语句，在菜名和用料查找并返回包含关键字的数据"""
    sql = '''select * from 全部菜品数据
        where 菜名 like "%{}%" or 用料 like "%{}%"'''.format(key, key)
    result = cursor.execute(sql)  # 接收查询结果
    data = []
    for item in result:  # 遍历查询结果并提取数据
        item = list(item)
        item[0] = emoji.emojize(item[0])
        item[1] = emoji.emojize(item[1])
        item[2] = emoji.emojize(item[2])
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
        else:
            data = select_all_data(key)
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
    else:
        data = select_all_data(key)
        if bool(data):
            print(data)  # 数据可视化使用
            print('来自数据库')
        else:  # 如果返回的数据为空，则实时查询
            url_list = get_url(url)
            data = get_data(url_list)
            print(data)  # 数据可视化使用
            print('来自实时数据')


if __name__ == '__main__':
    main()
