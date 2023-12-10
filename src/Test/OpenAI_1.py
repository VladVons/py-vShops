# 2023.12.08

import os
import asyncio
import aiohttp


class TOpenAI():
    def __init__(self):
        self.Url = "https://api.openai.com/v1/chat/completions"

        EnvKey = 'OPENAI_API_KEY'
        self.ApiKey = os.getenv(EnvKey)
        assert(self.ApiKey), f'cant read environment key `{EnvKey}`'

    async def Query(self, aMsg: str) -> str:
        Headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.ApiKey}"
        }

        Data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": aMsg}
            ]
        }

        async with aiohttp.ClientSession() as Session:
            async with Session.post(self.Url, json=Data, headers=Headers) as Response:
                if (Response.status == 200):
                    Data = await Response.json()
                    Res = Data["choices"][0]["message"]["content"]
                else:
                    Res = f"Err: {Response.status}, {Response.text}"
                return Res

async def Main():
    Prompt = "скільки буде людей на планеті у 2025р ?"
    OpenAI = TOpenAI()
    Response = await OpenAI.Query(Prompt)
    print(Response)

asyncio.run(Main())
