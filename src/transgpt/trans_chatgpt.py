#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------
# ChatGPT 翻译（国内需爬梯）
#   接口调用费用大约需要 $1/20万字
# ----------------------------------------------------


import os
import time
import openai
from ._settings import *
from ._trans_base import BaseTranslation

HTTP_PROXY = "HTTP_PROXY"
HTTPS_PROXY = "HTTPS_PROXY"

# GPT 接口模型定义 https://platform.openai.com/docs/models/
CHATGPT_35_TURBO = "gpt-3.5-turbo"
CHATGPT_4 = "gpt-4" # 8K
CHATGPT_4_32K = "gpt-4-32k"

ARG_ROLE = 'role'
ARG_OPENAI_MODEL = 'openai_model'
ARG_PROXY_IP = 'proxy_ip'
ARG_PROXY_PORT = 'proxy_port'

class ChatgptTranslation(BaseTranslation) :

    RETRY = 3
    RETRY_WAIT_SECONDS = 30

    def __init__(self, openai_key, openai_model=CHATGPT_35_TURBO, proxy_ip='127.0.0.1', proxy_port=0) :
        BaseTranslation.__init__(self, '', openai_key)
        openai.api_key = openai_key
        self.model = openai_model or CHATGPT_35_TURBO
        self.proxy = f"http://{proxy_ip}:{proxy_port}" if proxy_port > 0 else ""
        
    
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
        self._enable_proxy()
        msg = [
            role_setting, 
            {"role": "user", "content": segment}
        ]
        rsp = self._wait_for_ask(msg)
        rst = rsp.get("choices")[0]["message"]["content"]
        self._disable_proxy()
        return rst
    

    def _wait_for_ask(self, question) :
        rsp = ""
        for i in range(self.RETRY) :
            try :
                rsp = openai.ChatCompletion.create(
                    model=self.model,
                    messages=question
                )
                break

            except Exception as e:
                rsp = {
                    'choices': [{
                        'message': {
                            'content': f"[ERROR] ChatGPT No Response: {e}"
                        }
                    }]
                }
                time.sleep(self.RETRY_WAIT_SECONDS)
        return rsp


    def _enable_proxy(self) :
        os.environ[HTTP_PROXY] = self.proxy
        os.environ[HTTPS_PROXY] = self.proxy


    def _disable_proxy(self) :
        os.environ[HTTP_PROXY] = ""
        os.environ[HTTPS_PROXY] = ""

    
    def _len_limit(self) :
        return 500
    