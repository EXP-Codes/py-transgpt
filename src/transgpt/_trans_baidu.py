#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------
# 百度机翻器（比谷歌准确，且每个月有 200 万字的免费额度）
# ----------------------------------------------------

import time
import hashlib
import requests
import json
from _settings import *
from _trans_base import BaseTranslation
from color_log.clog import log


BAIDU_API_URL = "https://fanyi-api.baidu.com/api/trans/vip/translate"
ARG_API_URL = 'api_url'

class BaiduTranslation(BaseTranslation) :

    def __init__(self, api_id, api_key, api_url=BAIDU_API_URL) -> None :
        BaseTranslation.__init__(api_id, api_key, api_url)


    def _translate(self, segment, from_lang='en', to_lang='zh', args={}) :
        salt, sign = self._to_sign(segment)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'q': segment, 
            'from': from_lang, 
            'to': to_lang, 
            'appid': self.app_id, 
            'salt': salt, 
            'sign': sign
        }
        
        response = requests.post(self.url, headers=headers, data=body)
        trans_result = []
        try :
            if response.status_code == 200:
                rst = json.loads(response.text)
                for line in rst.get("trans_result") :
                    trans_result.append(line.get("dst").strip())
            else :
                log.error(f"翻译段落失败: 接口 [{response.status_code}] 异常")
        except :
            log.error(f"翻译段落失败: {response.text}")
        return DOUBLE_CRLF.join(trans_result)


    def _to_sign(self, data) :
        salt = int(time.time())
        sign = hashlib.md5(
            ("%s%s%i%s" % (
                self.app_id, 
                data,
                salt, 
                self.app_pass
            )).encode(encoding=CHARSET)
        ).hexdigest()
        return salt, sign


    def _len_limit(self) :
        return 2000
    