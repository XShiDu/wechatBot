# -*- coding: UTF-8 -*-
# 构造对话功能，一个机器人，用于和用户交流
import time
import hashlib
from lxml import etree
from flask import make_response    # 这些是本例中所有用到的库
from AIbot import ChatBot

class Bot:
    def __init__(self, apis):

        self.token = apis['wechat_params']['token']
        self.AppID = apis['wechat_params']['AppID']
        self.AppSecret = apis['wechat_params']['AppSecret']

        self.hash_table = {
            'text': ['Content'],
            'image': ['PicUrl', 'MediaId'],
            'voice': ['MediaId', 'Format'],
            'video': ['MediaId', 'ThumbMediaId'],
            'shortvideo': ['MediaId', 'ThumbMediaId'],
            'location': ['Location_X', 'Location_Y', 'Scale', 'Label'],
            'link': ['Title', 'Description', 'Url'],
        }

        self.bot = ChatBot(apis)

    def get_apply(self, req):
        # 该函数响应用于验证服务器接口的get请求
        signature = req.args.get('signature')  # 这里分别获取传入的四个参数
        timestamp = req.args.get('timestamp')
        nonce = req.args.get('nonce')
        echostr = req.args.get('echostr')
        return_code = 'Invalid'

        data = sorted([self.token, timestamp, nonce])  # 字典排序
        string = ''.join(data).encode('utf-8')  # 拼接成字符串
        hashcode = hashlib.sha1(string).hexdigest()  # sha1加密
        if signature == hashcode:
            return_code = echostr
        return return_code

    def post_apply(self, Content):
        #返回要回答的消息类型和消息
        MsgType, res = self.bot.chat(Content)
        return res

    def post_make_response(self, res, ToUserName, FromUserName):
        '''
        :param res: 回答
        :param ToUserName:
        :param FromUserName:
        :return:
        '''
        # 该函数用于响应用户输入
        xml = f'<xml><ToUserName><![CDATA[{FromUserName}]]></ToUserName>' \
              f'<FromUserName><![CDATA[{ToUserName}]]></FromUserName>' \
              f'<CreateTime>{str(int(time.time()))}</CreateTime>'
        #返回要回答的消息类型和消息
        MsgType = 'text'
        xml += f'<MsgType><![CDATA[{MsgType}]]></MsgType>' \
               f'<Content><![CDATA[{res}]]></Content></xml>'

        print(f'time:{time.time()}\tusername:{ToUserName}\treceivename:{FromUserName}\tcontent:{res}')
        response = make_response(xml)
        response.content_type = 'application/xml'
        return response

    def post_time_out(self, count):
        # 该函数用于响应用户输入
        #返回要回答的消息类型和消息
        if count == 3:
            res = "回复时间过长，超出微信接口响应时间，请等待几秒后重试或换一种方式提问，如在提问最后加上'回答不超过100字'"
        else:
            res = '请稍等，大模型生成回答中...'
        return res


    def post_receive(self, req):
        # 接收用户的输入
        xml = etree.fromstring(req.stream.read())
        MsgType = xml.find("MsgType").text
        ToUserName = xml.find("ToUserName").text
        FromUserName = xml.find("FromUserName").text
        CreateTime = xml.find("CreateTime").text
        MsgId = xml.find("MsgId").text


        # 获取用户输入类型
        attributes = self.hash_table[MsgType]   #获取大类型下的子类型

        # 提取用户输入中各类型具体输入
        Content = xml.find("Content").text if 'Content' in attributes else '抱歉，暂未支持此消息。'
        PicUrl = xml.find("PicUrl").text if 'PicUrl' in attributes else '抱歉，暂未支持此消息。'
        MediaId = xml.find("MediaId").text if 'MediaId' in attributes else '抱歉，暂未支持此消息。'
        Format = xml.find("Format").text if 'Format' in attributes else '抱歉，暂未支持此消息。'
        ThumbMediaId = xml.find("ThumbMediaId").text if 'ThumbMediaId' in attributes else '抱歉，暂未支持此消息。'
        Location_X = xml.find("Location_X").text if 'Location_X' in attributes else '抱歉，暂未支持此消息。'
        Location_Y = xml.find("Location_Y").text if 'Location_Y' in attributes else '抱歉，暂未支持此消息。'
        Scale = xml.find("Scale").text if 'Scale' in attributes else '抱歉，暂未支持此消息。'
        Label = xml.find("Label").text if 'Label' in attributes else '抱歉，暂未支持此消息。'
        Title = xml.find("Title").text if 'Title' in attributes else '抱歉，暂未支持此消息。'
        Description = xml.find("Description").text if 'Description' in attributes else '抱歉，暂未支持此消息。'
        Url = xml.find("Url").text if 'Url' in attributes else '抱歉，暂未支持此消息。'
        Recognition = xml.find("Recognition").text if 'Recognition' in attributes else '抱歉，暂未支持此消息。'
        #写入log
        print(f'time:{CreateTime}\tusername:{FromUserName}\treceivename:{ToUserName}\tcontent:{Content}')
        return Content, ToUserName, FromUserName


