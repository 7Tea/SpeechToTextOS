import webview
from flask import Flask, render_template, jsonify, request
import json
from functools import wraps

STATIC_FOLDER = 'static'
app = Flask(__name__, template_folder=STATIC_FOLDER, static_folder=STATIC_FOLDER)

def verify_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = json.loads(request.data)
        token = data.get('token')
        if token == webview.token:
            return function(*args, **kwargs)
        else:
            raise Exception('Authentication error')

    return wrapper


@app.route('/')
def index():
    return render_template('index.html', error='', token=webview.token)


if __name__ == '__main__':
    chinese = {
        'global.quitConfirmation': u'确定关闭?',
    }

    window = webview.create_window(
        title='视频语音识别',
        url=app,
        width=900,
        height=620,
        resizable=True,  # 固定窗口大小
        text_select=False,  # 禁止选择文字内容
        confirm_close=True,  # 关闭时提示
        min_size=(900, 620)
    )

    # window.closed += on_closed
    # window.closing += on_closing
    # window.shown += on_shown
    # window.loaded += on_loaded

    webview.start(localization=chinese, debug=True)

