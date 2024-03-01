
from flask import request
from flask import Flask
from chat_bot import Bot
import yaml

with open('./yamlData.yml', 'r', encoding='utf-8') as f:
    apis = yaml.load(f.read(), Loader=yaml.FullLoader)

bot = Bot(apis)


app = Flask(__name__)

@app.route("/wechat", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return bot.get_apply(request)

    elif request.method == "POST":
        return bot.post_apply(request)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

