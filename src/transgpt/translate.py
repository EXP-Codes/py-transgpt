#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------
# 文本翻译通用接口
# --------------------------------------------

from ._settings import *
from .trans_baidu import *
from .trans_tencent import *
from .trans_chatgpt import *
from color_log.clog import log


# 翻译平台
BAIDU = "baidu"
TENCENT = "tencent"
CHATGPT = "chatgpt"


def trans(content, api_id, api_key, 
            from_lang='', to_lang='', 
            platform=TENCENT, savepath='', oncesave=False, 
            cut_len=500, 
            args={}
    ) -> str:
    """
    翻译文本
    :param content      : 待翻译文本
    :param api_id       : 接口 API_ID / APP_ID （ChatGPT 不需要）
    :param api_key      : 接口 API_KEY / SECRET_KEY
    :param from_lang    : 待翻译文本的源语言（不同的平台语言代码不一样）
    :param to_lang      : 需要翻译的目标语言（不同的平台语言代码不一样）
    :param platform     : 翻译平台，目前支持： chatgpt, baidu, tencent（默认）
    :param savepath     : 翻译文本保存的位置，若为空则不保存（可通过返回值获取）
    :param oncesave     : 是否一次性保存翻译文本（对于超长文本，内部会进行分段翻译，为了避免网络异常导致已翻译文本丢失，此项默认关闭）
    :param cut_len      : 自动切割长文本的每一段长度（取决于 API 接口限制每次翻译的字数）
    :param args         : hash 其他参数表
                            api_url         : 仅百度翻译有用：接口 API 路径
                            region          : 仅腾讯翻译有用：翻译服务器所在的区域
                            UntranslatedText: 仅腾讯翻译有用：忽略的翻译文本
                            role            : 仅 ChatGPT 有用：AI 角色人设
                            openai_model    : 仅 ChatGPT 有用：OpenAPI 接口的大模型
                            proxy_ip        : 仅 ChatGPT 有用：网络代理服务 IP
                            proxy_port      : 仅 ChatGPT 有用：网络代理服务端口
    :return: 已翻译文本
    """

    log.info(f"正在使用 [{platform}] 翻译文本 ...")
    if platform == BAIDU :
        api_url = args.get(ARG_API_URL) or BAIDU_API_URL
        client = BaiduTranslation(api_id, api_key, api_url, cut_len)

    elif platform == CHATGPT :
        openai_model = args.get(ARG_OPENAI_MODEL) or CHATGPT_4o_MINI
        proxy_ip = args.get(ARG_PROXY_IP) or LOCALHOST
        proxy_port = args.get(ARG_PROXY_PORT) or 0
        response_format = args.get(ARG_RSP_FORMAT)
        client = ChatgptTranslation(api_key, openai_model, proxy_ip, proxy_port, cut_len, response_format)
    
    else :
        region = args.get(ARG_REGION) or GZ_REGION
        client = TencentTranslation(api_id, api_key, region, cut_len)

    trans_content = client.translate(content, from_lang, to_lang, savepath, oncesave, args)
    log.info(f"文本翻译完成")
    if savepath :
        log.info("翻译文本已%s存储到: %s" % ('' if oncesave else '分段', savepath))
    return trans_content
    
