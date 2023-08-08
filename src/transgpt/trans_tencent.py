#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------
# 腾讯机翻器（比谷歌准确，且每个月有 500 万字的免费额度）
# ----------------------------------------------------

from ._settings import *
from ._trans_base import BaseTranslation
from tencentcloud.common.credential import Credential
from tencentcloud.tmt.v20180321.tmt_client import TmtClient
from tencentcloud.tmt.v20180321.models import TextTranslateRequest
from tencentcloud.tmt.v20180321.models import TextTranslateResponse

GZ_REGION = 'ap-guangzhou'
ARG_REGION = 'region'
ARG_UNTRANSLATED_TEXT = 'UntranslatedText'

class TencentTranslation(BaseTranslation) :

    def __init__(self, api_id, api_key, region=GZ_REGION) :
        BaseTranslation.__init__(self, api_id, api_key)
        cred = Credential(api_id, api_key)
        self.client = TmtClient(cred, region)

    
    def _translate(self, segment, from_lang='en', to_lang='zh', args={}) :
        req = TextTranslateRequest()
        req.SourceText = segment
        req.Source = from_lang
        req.Target = to_lang
        req.ProjectId = 0
        req.UntranslatedText = args.get(ARG_UNTRANSLATED_TEXT) or ''   # 忽略的翻译文本
        rsp = self.client.TextTranslate(req)
        return rsp.TargetText


    def _len_limit(self) :
        return 2000
    
    
