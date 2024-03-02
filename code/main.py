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
    print(res)
    session[UserContent] = res


app = Flask(__name__)

@app.route("/wechat", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return bot.get_apply(request)

    elif request.method == "POST":
        UserContent, ToUsere, FromUser = bot.post_receive(request)
        # 创建子线程，如果没来得及处理，就主线程先回复，子线程将处理结果加入session
        sub_thread = threading.Thread(target=apply, args=(UserContent,))
        sub_thread.start()

        # 主线程等待子线程4秒
        sub_thread.join(4)

        # 若此回复四秒内运行不完
        if sub_thread.is_alive():
            #检测是否生成了回复，以及该提问请求的次数
            have_answer = session.get(UserContent, '')
            have_post_count = post_count.get(UserContent, 1)
            # 如果前面的请求已经生成了答案
            if have_answer:
                session.pop(UserContent)
                post_count.pop(UserContent)
                return bot.post_make_response(have_answer, ToUsere, FromUser)
            # 若没有生成答案
            else:
                # 判定是不是最后一次请求
                if have_post_count == 3:
                    res = bot.post_make_response(bot.post_time_out(3, UserContent), ToUsere, FromUser)
                    # 重置请求次数
                    post_count.pop(UserContent)
                else:
                    # res = bot.post_make_response(bot.post_time_out(have_post_count), ToUsere, FromUser)
                    res = 'success'
                    # 请求次数+1
                    post_count[UserContent] = have_post_count + 1
                return res
        # 运行完了，那肯定已经缓存了答案，直接返回即可
        else:
            answer = session[UserContent]
            return bot.post_make_response(answer, ToUsere, FromUser)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

