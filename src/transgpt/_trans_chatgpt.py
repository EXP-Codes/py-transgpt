#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------
# ChatGPT 翻译（国内需爬梯）
#   接口调用费用大约需要 $1/万字
# ----------------------------------------------------


import os
import openai
from _settings import *
from _trans_base import BaseTranslation

HTTP_PROXY = "HTTP_PROXY"
HTTPS_PROXY = "HTTPS_PROXY"
CHATGPT_35_TURBO = "gpt-3.5-turbo"
CHATGPT_4 = "gpt-4"
CHATGPT_4_32K = "gpt-4-32k"

ARG_ROLE = 'role'
ARG_OPENAI_MODEL = 'openai_model'
ARG_PROXY_IP = 'proxy_ip'
ARG_PROXY_PORT = 'proxy_port'

class ChatgptTranslation(BaseTranslation) :

    def __init__(self, openai_key, openai_model=CHATGPT_35_TURBO, proxy_ip='127.0.0.1', proxy_port=0) :
        BaseTranslation.__init__('', openai_key)
        openai.api_key = openai_key
        self.model = openai_model or CHATGPT_35_TURBO
        self.proxy = f"http://{proxy_ip}:{proxy_port}" if proxy_port > 0 else ""
        
    
    def _translate(self, segment, from_lang='英文', to_lang='中文', args={}) :
        role = args.get(ARG_ROLE) or f"您作为一个资深的专业翻译官，把下面文本中的{from_lang}内容翻译为{to_lang}，并润色（请勿回复翻译文本以外的内容）"
        role_setting = {"role": "system", "content": role}     # 设置 GPT 人设
        return self.ask_gpt(role_setting, segment)

    
    def ask_gpt(self, role_setting, segment) :
        self._enable_proxy()
        msg = [
            role_setting, 
            {"role": "user", "content": segment}
        ]
        rsp = openai.ChatCompletion.create(
          model=self.model,
          messages=msg
        )
        rst = rsp.get("choices")[0]["message"]["content"]
        self._disable_proxy()
        return rst


    def _enable_proxy(self) :
        os.environ[HTTP_PROXY] = self.proxy
        os.environ[HTTPS_PROXY] = self.proxy


    def _disable_proxy(self) :
        os.environ[HTTP_PROXY] = ""
        os.environ[HTTPS_PROXY] = ""

    
    def _len_limit(self) :
        return 500
    