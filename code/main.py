
from flask import request
from flask import Flask
from chat_bot import Bot
import yaml
import threading

with open('../api_config.yml', 'r', encoding='utf-8') as f:
    apis = yaml.load(f.read(), Loader=yaml.FullLoader)

bot = Bot(apis)


app = Flask(__name__)

@app.route("/wechat", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return bot.get_apply(request)

    elif request.method == "POST":
        # 开启一个新线程解决wx五秒不响应请求，失效的问题
        sub_thread = threading.Thread(target=bot.post_apply(request))
        sub_thread.start()
        # 主线程等待子线程4秒
        sub_thread.join(2)

        if sub_thread.is_alive():
            return bot.post_apply(request)
        else:
            return 'sucess'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

