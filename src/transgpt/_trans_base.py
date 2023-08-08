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

    def __init__(self, api_id, api_key) -> None :
        self.api_id = api_id
        self.api_key = api_key


    def translate(self, content, from_lang='', to_lang='', savepath='', oncesave=False, args={}) -> str :
        self.oncesave = oncesave    # False: 分段保存； True: 一次性保存
        trans_result = []
        segments = self._cut(content)
        log.info("切割为 [%i] 段翻译 ..." % len(segments))

        cnt = 0
        for seg in segments :
            cnt += 1
            log.info("正在翻译第 [%i] 段 ..." % cnt)
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
        return 500  # API 接口限制每次翻译的字数
    

    @abstractmethod
    def _translate(self, segment, from_lang='en', to_lang='zh', args={}) -> str :
        # TODO 子类实现
        return ""

