#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------

CHARSET = 'UTF-8'
DOUBLE_CRLF = "\n\n"

# 翻译提供商
BAIDU = "baidu"
TENCENT = "tencent"
CHATGPT = "chatgpt"


 # 百度/腾讯限制一次只能翻译 2000 个字符
 # chatgpt 一次只能返回 500 个单词
 # 按这个标准对被翻译的内容进行分段切割（取最小值）
SPLIT_SEG_LIMIT = 500

