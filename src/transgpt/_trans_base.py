#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------

import os
import time
from ._settings import *
from abc import ABCMeta, abstractmethod     # python不存在抽象类的概念， 需要引入abc模块实现
from color_log.clog import log


class BaseTranslation :

    __metaclass__ = ABCMeta # 定义为抽象类

    def __init__(self, api_id, api_key, cut_len=500) -> None :
        """
        翻译文本
        :param api_id  : 接口 API_ID / APP_ID （ChatGPT 不需要）
        :param api_key : 接口 API_KEY / SECRET_KEY
        :param cut_len : 自动切割长文本的每一段长度（取决于 API 接口限制每次翻译的字数）
        """
        self.api_id = api_id
        self.api_key = api_key
        self.cut_len = cut_len


    def translate(self, content, from_lang='', to_lang='', savepath='', oncesave=False, args={}) -> str :
        """
        翻译文本
        :param content   : 待翻译文本
        :param from_lang : 待翻译文本的源语言（不同的平台语言代码不一样）
        :param to_lang   : 需要翻译的目标语言（不同的平台语言代码不一样）
        :param savepath  : 翻译文本保存的位置，若为空则不保存（可通过返回值获取）
        :param oncesave  : 是否一次性保存翻译文本（对于超长文本，内部会进行分段翻译，为了避免网络异常导致已翻译文本丢失，此项默认关闭）
        :param args      : hash 其他参数表
                            api_url         : 仅百度翻译有用：接口 API 路径
                            region          : 仅腾讯翻译有用：翻译服务器所在的区域
                            UntranslatedText: 仅腾讯翻译有用：忽略的翻译文本
                            role            : 仅 ChatGPT 有用：AI 角色人设
                            openai_model    : 仅 ChatGPT 有用：OpenAPI 接口的大模型
                            proxy_ip        : 仅 ChatGPT 有用：网络代理服务 IP
                            proxy_port      : 仅 ChatGPT 有用：网络代理服务端口
        :return: 已翻译文本
        """
        
        self.oncesave = oncesave    # False: 分段保存； True: 一次性保存
        trans_result = []
        segments = self._cut(content)
        log.debug("切割为 [%i] 段翻译 ..." % len(segments))

        cnt = 0
        for seg in segments :
            cnt += 1
            log.debug("正在翻译第 [%i] 段 ..." % cnt)
            trans_segment = self._translate(seg, from_lang, to_lang, args)
            trans_result.append(trans_segment)
            if not self.oncesave :
                self._save_trans(trans_segment, savepath)
            time.sleep(1)

        trans_content = DOUBLE_CRLF.join(trans_result)
        if self.oncesave :
            self._save_trans(trans_content, savepath)
        return trans_content


    # 翻译接口每次调用有字数限制，过长文本需要分段翻译。
    def _cut(self, content) :
        if self._len_limit() <= 0 :
            return [ content ]
        
        segments = []
        seg = []
        seg_len = 0

        # 为了避免语义问题，此处会使用换行符对文本进行多段切割，
        lines = content.split(CRLF)
        for line in lines :
            line = line.strip()
            if not line :
                continue

            # 然后按顺序重新组装为“不大于限制字数”的段落
            line_len = len(line)
            if seg_len + line_len > self._len_limit() :
                segments.append(CRLF.join(seg))
                seg_len = 0
                seg = []

            seg.append(line)
            seg_len += line_len

        segments.append(DOUBLE_CRLF.join(seg))
        return segments
    

    def _save_trans(self, content, savepath) :
        if not savepath :
            return
        
        save_dir = os.path.dirname(savepath)
        try :
            os.makedirs(save_dir)
        except :
            pass

        if self.oncesave :
            with open(savepath, "w+", encoding=CHARSET) as file :
                file.write(content)
            log.info(f"翻译完成，译文已存储到 [{savepath}]")

        else :
            with open(savepath, "a+", encoding=CHARSET) as file :
                file.write(content)
            log.info(f"段翻译完成，译文已追加存储到 [{savepath}]")


    
    @abstractmethod
    def _len_limit(self) :
        return self.cut_len
    

    @abstractmethod
    def _translate(self, segment, from_lang='en', to_lang='zh', args={}) -> str :
        # TODO 子类实现
        return ""

