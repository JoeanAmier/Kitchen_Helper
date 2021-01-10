import time
import random
import sqlite3
from requests_html import HTMLSession
import re
import emoji


def get_page_url():
    """返回每页的网址"""
    list = []
    base = 'http://www.xiachufang.com/explore/?page='
    for page in range(1, 2):
        """生成 1 ~ 20 页的网页地址"""
        url = base + str(page)
        list.append(url)
    return list  # 返回 1 ~ 20 页的地址


def get_url(list):
    """获取每个菜品的详细链接"""
    item_url = []
    for page in list:  # 遍历每一页的网址
        html = open_url(page)  # 请求网页
        time.sleep(random.randrange(4, 7, 1))  # 减慢爬取速度
        href = html.html.find(
            '.recipe.recipe-215-horizontal.pure-g.image-link.display-block > a')  # 查找每一个菜品的详细链接
        for url in href:
            item_url.append(
                'http://www.xiachufang.com' +
                url.attrs['href'])  # 拼接每一个菜品的详细链接
    return item_url  # 返回 1 ~ 20 页的全部菜品详细链接


def open_url(url):
    session = HTMLSession()
    response = session.get(url)  # 向网页发送请求
    return response  # 返回网页响应


def get_data(url_list):
    data = []  # 储存总数据
    for item in url_list:  # 遍历每一个菜品的详细链接
        cache = []  # 储存每个菜品的数据
        html = open_url(item)  # 发送请求
        if str(html) == '<Response [200]>':  # 判断是否请求成功
            time.sleep(random.randrange(4, 7, 1))  # 减慢爬取速度
            title = html.html.find('.page-title')  # 匹配菜名
            if bool(title):  # 判断匹配结果
                title = emoji.demojize(title[0].text)
                cache.append(title)  # 添加有效数据
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
            recipeIngredient = html.html.find('.ings')  # 匹配用料
            if bool(recipeIngredient):  # 判断匹配结果
                recipeIngredient = emoji.demojize(recipeIngredient[0].text)
                cache.append(recipeIngredient)  # 添加有效数据
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
            recipeInstructions = html.html.find('.steps p.text')  # 匹配做法步骤
            if bool(recipeInstructions):  # 判断匹配结果
                """这里匹配的结果是包含多项的列表，要先处理成单个字符串再添加有效数据"""
                steps = ''
                for i in range(len(recipeInstructions)):
                    """遍历匹配结果，这个数据是做法步骤，不同菜品的步骤数不相等，通过遍历组成单个字符串"""
                    steps += recipeInstructions[i].text
                cache.append(emoji.demojize(steps))  # 添加有效数据
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
            image = html.html.find(
                'div.cover.image.expandable.block-negative-margin > img')  # 匹配效果图链接
            if bool(image):  # 判断匹配结果
                cache.append(image[0].attrs['src'])  # 添加有效数据
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
            url = html.html.find('link[rel=canonical]')  # 匹配详细链接
            if bool(url):  # 判断匹配结果
                cache.append(url[0].attrs['href'])  # 添加有效数据
                find = re.compile(
                    r'https://www.xiachufang.com/recipe/([0-9]+?)/')
                id = re.findall(find, url[0].attrs['href'])
                if id:
                    cache.append(id[0])
                else:
                    print(id)
                    cache.append('')
            else:
                print(item)  # 输出检查以便判断问题
                cache.append('')  # 添加空数据，避免直接报错
            data.append(cache)  # 添加一个菜品的数据到总数据
        else:
            break  # 请求失败说明被封IP，跳出循环，爬取结束
    return data  # 返回总数据的列表


def save_data(data):
    sqlite = sqlite3.connect('菜品数据库.db')  # 连接数据库
    cursor = sqlite.cursor()  # 获取数据库游标
    try:
        """尝试删除旧表"""
        sql = 'DROP TABLE 本周最受欢迎'  # 删除旧表
        cursor.execute(sql)  # 执行SQL语句，如果需要不删除旧表可以注释此段代码
        sqlite.commit()  # 提交更改
    except BaseException:
        pass
    finally:
        sql = '''create table 本周最受欢迎
        ('菜名' text,
        '用料' text,
        '做法' text,
        '效果图' text,
        '链接' text,
        'ID' text primary key)'''  # 创建表
        cursor.execute(sql)  # 执行SQL语句
        sqlite.commit()  # 提交更改
    for item in data:  # 遍历保存数据
        for index in range(len(item)):  # 数据预处理，SQL语句格式要求
            item[index] = '"' + str(item[index]) + '"'
        sql = '''insert into 本周最受欢迎
        values(%s)''' % ', '.join(item)  # 插入数据
        cursor.execute(sql)  # 执行SQL语句
        sqlite.commit()  # 提交更改
    sqlite.close()  # 关闭数据库


def all_data(data):
    sqlite = sqlite3.connect('菜品数据库.db')  # 连接数据库
    cursor = sqlite.cursor()  # 获取数据库游标
    try:
        sql = '''create table 全部菜品数据
                ('菜名' text,
                '用料' text,
                '做法' text,
                '效果图' text,
                '链接' text,
                'ID' text primary key)'''  # 创建表
        cursor.execute(sql)  # 执行SQL语句
        sqlite.commit()  # 提交更改
    except BaseException:
        pass
    for item in data:  # 遍历保存数据
        sql = '''insert or ignore into 全部菜品数据
        values(%s)''' % ', '.join(item)  # 插入数据
        cursor.execute(sql)  # 执行SQL语句
        sqlite.commit()  # 提交更改
    sqlite.close()  # 关闭数据库


def main():
    list = get_page_url()  # 生成每一页的网址
    url = get_url(list)  # 获取 1 ~ 20 页的全部菜品详细链接
    data = get_data(url)  # 提取数据
    save_data(data)  # 保存数据
    all_data(data)


if __name__ == '__main__':
    main()
