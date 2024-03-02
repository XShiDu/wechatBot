import time

from flask import Flask, make_response, request
from chat_bot import Bot
import yaml
from lxml import etree
import threading

with open('../api_config.yml', 'r', encoding='utf-8') as f:
    apis = yaml.load(f.read(), Loader=yaml.FullLoader)

bot = Bot(apis)
# 若时间不过，用于缓存用户的提问和结果(微信三次重复请求中，只有content是一致的，且用户间是区分性质的)
session = {}
# 缓存请求次数
post_count = {}


def apply(UserContent):
    res = bot.post_apply(UserContent)
    session[UserContent] = res


app = Flask(__name__)

@app.route("/wechat", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return bot.get_apply(request)

    elif request.method == "POST":
        UserContent, ToUsere, FromUser = bot.post_receive(request)

        # 先判定前面的请求有没有生成回答
        front_answer = session.get(UserContent, '')
        front_post_count = post_count.get(UserContent, 0)
        if front_answer:
            # 清楚缓存
            session.pop(UserContent)
            return bot.post_make_response(front_answer, ToUsere, FromUser)

        # 如果是第一次请求, post_count无该问题缓存
        if front_post_count == 0:
            # 创建子线程，如果没来得及处理，就主线程不回复，直接超时，等待微信重复请求，子线程继续处理，结果加入session
            sub_thread = threading.Thread(target=apply, args=(UserContent,))
            sub_thread.start()
            # 主线程等待子线程4秒
            sub_thread.join(4)
            # 若此回复四秒内运行不完
            if sub_thread.is_alive():
                # 那么等待请求过期
                post_count[UserContent] = 1
                res = bot.post_time_out(0, UserContent)
                time.sleep(1)
            # 若运行完了
            else:
                # 提取运行结果
                res = session[UserContent]
                # 清除缓存
                session.pop(UserContent)
            return bot.post_make_response(res, ToUsere, FromUser)
        # 是第二次请求，第一次过期了
        elif front_post_count == 1:
            # 等待4s
            time.sleep(4)
            # 判定第一次请求子线程结果有没有
            if UserContent in session:
                # 提取运行结果
                res = session[UserContent]
                # 清除缓存
                session.pop(UserContent)
                post_count.pop(UserContent)
            else:
                post_count[UserContent] = 2
                res = bot.post_time_out(1, UserContent)
                time.sleep(1)
            return bot.post_make_response(res, ToUsere, FromUser)
        # 是第三次请求了， 第二次请求期间没有得到响应，不管有没有，都返回答案
        else:
            # 等待4s
            time.sleep(4)
            # 判定第一次请求子线程结果有没有
            if UserContent in session:
                # 提取运行结果
                res = session[UserContent]
                # 清除缓存
                session.pop(UserContent)
            else:
                res = bot.post_time_out(2, UserContent)
            # 最后一次请求，清除请求计数缓存
            post_count.pop(UserContent)
            return bot.post_make_response(res, ToUsere, FromUser)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

