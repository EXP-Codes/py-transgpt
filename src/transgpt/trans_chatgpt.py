#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------
# ChatGPT 翻译（国内需爬梯）
#   接口调用费用大约需要 $1/20万字
# ----------------------------------------------------


import time
import httpx
from openai import OpenAI
from ._settings import *
from ._trans_base import BaseTranslation


# GPT 接口模型定义 https://platform.openai.com/docs/models/
CHATGPT_35_TURBO = "gpt-3.5-turbo"          # 16K
CHATGPT_4 = "gpt-4"                         # 8K
CHATGPT_4_TRUBO = "gpt-4-turbo"             # 128K
CHATGPT_4o = "gpt-4o"                       # 128K（静态模型，适合翻译）
CHATGPT_4o_20240806 = "gpt-4o-2024-08-06"   # 128K（静态模型，100% 格式化输出）
CHATGPT_4o_LATEST = "chatgpt-4o-latest"     # 128K（动态模型，价格高）
CHATGPT_4o_MINI = "gpt-4o-mini"             # 128K（翻译较弱）

HTTP_PROXY = "HTTP_PROXY"
HTTPS_PROXY = "HTTPS_PROXY"

ARG_ROLE = 'role'
ARG_OPENAI_MODEL = 'openai_model'
ARG_PROXY_IP = 'proxy_ip'
ARG_PROXY_PORT = 'proxy_port'
ARG_RSP_FORMAT = 'response_format'
# 关于 response_format : 
#   ChatGPT-4o-mini 模型的新特性，支持返回内容格式化为 json_schema
# 例如希望 openai 返回 { 'id': 1, 'name': 'xxxx', 'desc': 'yyyy' }
# 那么可以定义：
# response_format = {
#     "type": "json_schema",
#     "json_schema": {
#         "name": "response_schema",
#         "strict": True,
#         "schema": {
#             "type": "object",
#             "properties": {
#                 "id": {
#                     "type": "integer"
#                 },
#                 "name": {
#                     "type": "string"
#                 },
#                 "desc": {
#                     "type": "string"
#                 }
#             },
#             "required": ["id", "name", "desc"],
#             "additionalProperties": False
#         }
#     }
# }

class ChatgptTranslation(BaseTranslation) :

    RETRY = 3
    RETRY_WAIT_SECONDS = 30

    def __init__(self, openai_key, openai_model=CHATGPT_4o_MINI, proxy_ip='127.0.0.1', proxy_port=0, cut_len=500, response_format=None) :
        BaseTranslation.__init__(self, '', openai_key, cut_len)
        proxy = f"http://{proxy_ip}:{proxy_port}" if proxy_port > 0 else ""
        proxies = { "http://": proxy, "https://": proxy, }
        http_cli = httpx.Client(proxies=proxies) if proxy else None

        self.ai_cli = OpenAI(api_key=openai_key, http_client=http_cli)
        self.response_format = response_format
        self.model = openai_model or CHATGPT_4o_MINI
        
    
    def _translate(self, segment, from_lang='英文', to_lang='中文', args={}) :
        """
        翻译文本段落
        :param segment   : 待翻译文本段落
        :param from_lang : 待翻译文本的源语言（不同的平台语言代码不一样）
        :param to_lang   : 需要翻译的目标语言（不同的平台语言代码不一样）
        :param args      : hash 其他参数表
                            role : AI 角色人设
        :return: 已翻译的文本段落
        """
        role = args.get(ARG_ROLE) or f"您作为一个资深的专业翻译官，把下面文本中的{from_lang}内容翻译为{to_lang}，并润色（请勿回复翻译文本以外的内容）"
        role_setting = {"role": "system", "content": role}     # 设置 GPT 人设
        return self._ask_gpt(role_setting, segment)

    
    def _ask_gpt(self, role_setting, segment) :
        msg = [
            role_setting, 
            { "role": "user", "content": segment }
        ]
        answer = self._wait_for_ask(msg)
        return answer
    

    def _wait_for_ask(self, question) :
        answer = ""
        for i in range(self.RETRY) :
            try :
                rsp = self.ai_cli.chat.completions.create(
                    model=self.model,
                    messages=question, 
                    response_format=self.response_format
                )
                answer = rsp.choices[0].message.content
                break

            except Exception as e :
                answer = f"[ERROR] ChatGPT No Response: {e}"
                time.sleep(self.RETRY_WAIT_SECONDS)
        return answer
