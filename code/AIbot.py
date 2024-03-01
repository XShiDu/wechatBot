from zhipuai import ZhipuAI

class ChatBot():
    def __init__(self, apis):
        self.model = apis['model_params']['model']
        self.api_key=apis['model_params']['api_key']
        self.init_prompt = apis['model_params']['init_prompt']

        self.message = [
            {"role": "system", "content": self.init_prompt},

        ]

    def get_user(self, input):
        self.message.append({"role": "user", "content": input})

    def get_response(self):
        client = ZhipuAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,  # 填写需要调用的模型名称
            messages=self.message,
        )
        res = str(response.choices[0].message).split('role')[0][9:-2]
        return res

    def chat(self, input):
        self.get_user(input)
        res = self.get_response()
        return 'text', res