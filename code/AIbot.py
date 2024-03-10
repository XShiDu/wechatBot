from zhipuai import ZhipuAI
from random import choice
from utils import get_stock_industry, get_company_info, get_stock_index, get_history_manager, get_history_director
from utils import get_history_supervisors, get_history_share, get_history_seo, restrict_stock_open

class ChatBot():
    def __init__(self, apis):
        self.model = apis['model_params']['model']
        self.api_key=choice(apis['model_params']['api_key'])['key']
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
                    "required": ["code", "iscode"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_company_info",
                "description": "根据用户提供的信息，查询股票对应的公司简介、基本信息",
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
                    "required": ["code", "iscode"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_stock_index",
                "description": "根据用户提供的信息，查询股票对应的所属指数",
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
                    "required": ["code", "iscode"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_history_manager",
                "description": "根据用户提供的信息，查询股票对应公司的高管信息、历届高管成员",
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
                    "required": ["code", "iscode"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_history_director",
                "description": "根据用户提供的信息，查询股票对应公司的董事信息、历届董事会成员",
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
                    "required": ["code", "iscode"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_history_supervisors",
                "description": "根据用户提供的信息，查询股票对应公司的监事信息、历届监事会成员",
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
                    "required": ["code", "iscode"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_history_share",
                "description": "根据用户提供的信息，查询股票对应的公司近年的分红情况，当前为2024年",
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
                        "start_year": {
                            "type": "string",
                            "description": "要查询的开始时间的年份，如2023",
                        },
                        "end_year": {
                            "type": "string",
                            "description": "要查询的结束时间的年份，如2024",
                        },
                    },
                    "required": ["code", "iscode", "start_year", "end_year"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_history_seo",
                "description": "根据用户提供的信息，查询股票对应的公司近年的增发情况，当前为2024年",
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
                        "start_year": {
                            "type": "string",
                            "description": "要查询的开始时间的年份，如2023",
                        },
                        "end_year": {
                            "type": "string",
                            "description": "要查询的结束时间的年份，如2024",
                        },
                    },
                    "required": ["code", "iscode", "start_year", "end_year"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "restrict_stock_open",
                "description": "根据用户提供的信息，查询股票对应的公司近年的解禁限售情况，当前为2024年",
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
                        "start_year": {
                            "type": "string",
                            "description": "要查询的开始时间的年份，如2023",
                        },
                        "end_year": {
                            "type": "string",
                            "description": "要查询的结束时间的年份，如2024",
                        },
                    },
                    "required": ["code", "iscode", "start_year", "end_year"],
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
            # id = response.choices[0].message.tool_calls[0].id
            content_clsass, res = eval(func)(**eval(arg))
            # self.message.append({"role": "tool", "content": res, "tool_call_id":id})
            self.message.pop(-1)
        else:
            res = response.choices[0].message.content
            content_clsass = 'text'
            self.message.append({"role": "assistant", "content": res})
        return content_clsass, res

    def chat(self, input):
        self.get_user(input)
        content_clsass, res = self.get_response()
        # print(self.message)

        return content_clsass, res