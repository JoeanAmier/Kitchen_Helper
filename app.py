from flask import Flask
from 厨房好帮手 import select
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        keyword = request.form['keyword']
        source, data = select(keyword)
        return render_template('result.html', source=source, data=data)
    else:
        return '无效参数'


if __name__ == '__main__':
    app.run()
