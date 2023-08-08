# py-transgpt

> python 长文本多平台翻译器（目前支持 baidu、tencent、chatgpt）

------

## 简介

封装了 baidu、tencent、chatgpt 翻译平台的接口的差异性，只需要简单几步配置即可使用。

同时支持长文本翻译：原生的平台接口有字数限制，但是 [transgpt](https://github.com/EXP-Codes/py-transgpt) 会自动切割长文本为多段再调用接口翻译、翻译结果自动拼接为长文本。


## 运行环境

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)


## 安装说明

执行脚本：

```
python -m pip install --upgrade pip
python -m pip install py-transgpt
```

## 使用说明

### 百度翻译

> 使用前需要先到 [百度翻译开放平台](https://fanyi-api.baidu.com/manage/developer) 生成 API Key

```python
# 使用方法 1
from transgpt.translate import trans, BAIDU
result = trans(
    ${CONTENT}, 
    from_lang='jp', 
    to_lang='zh', 
    platform=BAIDU, 
    api_id=${BD_APP_ID}, 
    api_key=${BD_APP_KEY}
)

# 使用方法 2
from transgpt.trans_baidu import BaiduTranslation
client = BaiduTranslation(api_id=${BD_APP_ID}, api_key=${BD_APP_KEY})
result = client.translate(${CONTENT}, from_lang='jp', to_lang='zh')
```

更多使用方法详见单元测试：

- [使用方法 1](https://github.com/EXP-Codes/py-transgpt/blob/ae843092be17c53cfd40686129fa9e2976418042/test/test.py#L70)
- [使用方法 2](https://github.com/EXP-Codes/py-transgpt/blob/ae843092be17c53cfd40686129fa9e2976418042/test/test.py#L84)

![](./imgs/baidu.jpg)


### 腾讯翻译

> 使用前需要先到 [腾讯云机器翻译](https://console.cloud.tencent.com/cam/capi) 生成 API Key

```python
# 使用方法 1
from transgpt.translate import trans, TENCENT
result = trans(
    ${CONTENT}, 
    from_lang='jp', 
    to_lang='zh', 
    platform=TENCENT, 
    api_id=${TX_SECRET_ID}, 
    api_key=${TX_SECRET_KEY}
)

# 使用方法 2
from transgpt.trans_tencent import TencentTranslation
client = TencentTranslation(api_id=${BD_APP_ID}, api_key=${BD_APP_KEY})
result = client.translate(${CONTENT}, from_lang='jp', to_lang='zh')
```

更多使用方法详见单元测试：

- [使用方法 1](https://github.com/EXP-Codes/py-transgpt/blob/ae843092be17c53cfd40686129fa9e2976418042/test/test.py#L109)
- [使用方法 2](https://github.com/EXP-Codes/py-transgpt/blob/ae843092be17c53cfd40686129fa9e2976418042/test/test.py#L127)

![](./imgs/tencent.jpg)


### ChatGPT AI 翻译

> 使用前需要先到 [OpenAI](https://platform.openai.com/account/api-keys) 生成 API Key

```python
# 使用方法 1
from transgpt.translate import trans, CHATGPT, CHATGPT_35_TURBO
result = trans(
    ${CONTENT}, 
    platform=CHATGPT, 
    api_id='', 
    api_key=${GPT_API_KEY}, 
    args={
        ARG_ROLE: ${GPT_AI_ROLE},     # Option: 定义人设
        ARG_OPENAI_MODEL: CHATGPT_35_TURBO, 
        ARG_PROXY_IP: '127.0.0.1', 
        ARG_PROXY_PORT: 8888
    }
)

# 使用方法 2
from transgpt.trans_chatgpt import ChatgptTranslation, CHATGPT_35_TURBO, ARG_ROLE
client = ChatgptTranslation(${GPT_API_KEY}, CHATGPT_35_TURBO, '127.0.0.1', 8888)
result = client.translate(${CONTENT}, from_lang='日文', to_lang='中文')     # 使用内置 AI 人设
result = client.translate(${CONTENT}, args={ ARG_ROLE: ${GPT_AI_ROLE} })    # 使用自定义 AI 人设
```

更多使用方法详见单元测试：

- [使用方法 1](https://github.com/EXP-Codes/py-transgpt/blob/ae843092be17c53cfd40686129fa9e2976418042/test/test.py#L156)
- [使用方法 2](https://github.com/EXP-Codes/py-transgpt/blob/ae843092be17c53cfd40686129fa9e2976418042/test/test.py#L176)

![](./imgs/chatgpt.jpg)

