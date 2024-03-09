from zhipuai import ZhipuAI
from utils import get_stock_industry

class ChatBot():
    def __init__(self, apis):
        self.model = apis['model_params']['model']
        self.api_key=apis['model_params']['api_key']
        self.init_prompt = apis['model_params']['init_prompt']

        self.message = [
            {"role": "system", "content": self.init_prompt},

        ]
        self.tools = [
        {
            "type": "function",
            "function": {
                "name": "get_stock_industry",
                "description": "根据用户提供的信息，查询股票对应的行业、概念和板块",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "股票名称或代码",
                        },
                        "iscode": {
                            "type": "string",
                            "description": "判断是股票名称还是股票代码，是股票代码时为1，是股票名称时为0",
                        },
                    },
                    "required": ["code", "iscode", "date"],
                },
            }
        }
        ]

    def get_user(self, input):
        self.message.append({"role": "user", "content": input})

    def get_response(self):
        client = ZhipuAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,  # 填写需要调用的模型名称
            messages=self.message,
            tools=self.tools,
            tool_choice="auto",
        )
        if response.choices[0].message.tool_calls:
            func = response.choices[0].message.tool_calls[0].function.name
            arg = response.choices[0].message.tool_calls[0].function.arguments
            content_clsass, res = eval(func)(**eval(arg))
        else:
            res = response.choices[0].message.content
            content_clsass = 'text'
        self.message.append({"role": "assistant", "content": res})
        return content_clsass, res

    def chat(self, input):
        self.get_user(input)
        content_clsass, res = self.get_response()

        return content_clsass, res