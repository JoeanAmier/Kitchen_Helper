from flask import Flask
from 厨房好帮手 import select
from flask import render_template
from flask import request
from referer import clear
from referer import download

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/result/', methods=['GET', 'POST'])
def result():
    clear()  # 检查缓存目录
    if request.method == 'POST':
        keyword = request.form['keyword']
        if keyword:
            source, data = select(keyword)
            cache = [[i[5], i[3]] for i in data]
            for i in cache:
                download(i[0], i[1])  # 下载效果图
            return render_template(
                'result_modify.html', source=source, data=data)
            # return render_template(
            #     'result.html', source=source, data=data)
        else:
            return '无效参数'
    else:
        return '无效参数'


if __name__ == '__main__':
    app.run()
