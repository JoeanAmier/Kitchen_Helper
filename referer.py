import requests
import os


def clear():
    """检查效果图缓存目录，若缓存图片超过100时清理文件夹"""
    root = os.getcwd() + r'\static\cache'
    if os.path.exists(root):
        cache = os.listdir(root)
        if len(cache) >= 100:
            for file in cache:
                path = root + '\\' + file
                os.remove(path)
        else:
            return
    else:
        return


def download(id, url):
    """下载效果图到本地，name为菜名，url为效果图链接"""
    root = os.getcwd() + r'\static\cache'
    if not os.path.exists(root):
        os.mkdir(root)  # 缓存目录不存在时创建文件夹
    path = root + '\\' + id + '.jpg'
    if os.path.exists(path):  # 效果图已存在时直接返回
        return
    headers = {
        'accept': 'text/html,pplication/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,ap'
                  'plication/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.xiachufang.com/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.428'
                      '0.66 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
            f.close()
    else:
        print('获取图片失败', url, response.status_code)


def main():
    file = input('输入效果图ID：')
    url = input('输入效果图链接：')
    clear()
    download(file, url)


if __name__ == '__main__':
    main()
