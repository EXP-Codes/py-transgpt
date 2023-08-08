#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
# ----------------------------------------------------------------------
# 把父级目录（项目根目录）添加到工作路径，以便在终端也可以执行单元测试
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import unittest
from src.transgpt.translate import *
from src.transgpt.trans_baidu import *
from src.transgpt.trans_tencent import *
from src.transgpt.trans_chatgpt import *


class TestScenes(unittest.TestCase):

    @classmethod
    def setUpClass(cls) :
        pass


    @classmethod
    def tearDownClass(cls) :
        pass


    def setUp(self) :
        # Baidu 生成 API Key https://fanyi-api.baidu.com/manage/developer
        self.BD_APP_ID = 'xxxxxxxxxxxxxxxx'
        self.BD_APP_KEY = 'yyyyyyyyyyyyyyyy'
        self.BD_SAVE_PATH = './test/output/result_baidu.txt'

        # Tencent 生成 API Key https://console.cloud.tencent.com/cam/capi
        self.TX_SECRET_ID = 'xxxxxxxxxxxxxxxx'
        self.TX_SECRET_KEY = 'yyyyyyyyyyyyyyyy'
        self.TX_SAVE_PATH = './test/output/result_tencent.txt'

        # ChatGPT 生成 API Key https://platform.openai.com/account/api-keys
        self.GPT_API_KEY = 'sk-xxxxxxxxxxxxxxxx'
        self.GPT_AI_ROLE = '基于《从零开始的异世界生活》小说的背景，把日文内容翻译成中文，并润色'
        self.GPT_SAVE_PATH = './test/output/result_chatgpt.txt'

        # 待翻译文本
        self.CONTENT = '''
「――村長くん、ちょっといいかい？」
そう背中から声をかけられ、ヴィンセント・ヴォラキアは足を止めた。
振り向く前から、声の相手はわかっている。一度聞いた声や、目にした相手のことは忘れない。これもすぐ、金髪に青い目をした行商人――フロップ・オコーネルとわかった。
「生憎、今は帝国存亡の危機だ。貴様の雑話にかまけている時間はない」
わかったが、わかった上でヴィンセントは取り合わない。
今しがた受け取った『星詠み』ウビルクの託宣、その扱いについてベルステツやセリーナたちと協議しなくてはならない。
敵への対抗策になると指名されたグルービーだが、死んでいる可能性が高い以上、それを当てにした計画を立てるなどと愚の骨頂だ。その点、指名されたもう一人の説得に向かったナツキ・スバルに期待する方が、まだマシな愚考と言えるだろう。
そもそも、あの少女を説得できる目はヴィンセントにはない。
彼女とはまともな意思疎通さえままならないのだ。ヴィンセントの持つ手札が少女に通用しない以上、二つの光の片方はスバルに掴み取らせるのが道理。
故に、ヴィンセントにできるのは現実的な策の検討の積み重ねだけ――、
「おっとっと、雑話かどうかは話してみなくちゃわからないことじゃないかな！僕がどんな話のタネを持っているか、いくら賢い村長くんでも水撒きする前からわかったりはしないだろうに！」
'''


    def tearDown(self) :
        pass


    # 使用 baidu 翻译（通用接口, 最全参数）
    def test_baidu_trans_1(self) :
        result = trans(
            self.CONTENT, 
            from_lang='jp', 
            to_lang='zh', 
            platform=BAIDU, 
            api_id=self.BD_APP_ID, 
            api_key=self.BD_APP_KEY, 
            savepath=self.BD_SAVE_PATH, 
            oncesave=True, 
        )


    # 使用 baidu 翻译（专用接口）
    def test_baidu_trans_2(self) :
        client = BaiduTranslation(
            api_id=self.BD_APP_ID, 
            api_key=self.BD_APP_KEY, 
            api_url=BAIDU_API_URL            # Option: 百度一般不会更换 API URL
        )

        # 最少参数（写文件）
        result = client.translate(
            self.CONTENT, 
            from_lang='jp',
            to_lang='zh',
            savepath=self.BD_SAVE_PATH, 
            oncesave=True
        )

        # 最少参数（仅内存）
        result = client.translate(
            self.CONTENT, 
            from_lang='jp',
            to_lang='zh'
        )


    # 使用 tencent 翻译（通用接口, 最全参数）
    def test_tencent_trans_1(self) :
        result = trans(
            self.CONTENT, 
            from_lang='jp', 
            to_lang='zh', 
            platform=TENCENT, 
            api_id=self.TX_SECRET_ID, 
            api_key=self.TX_SECRET_KEY, 
            savepath=self.TX_SAVE_PATH, 
            oncesave=True, 
            args={
                ARG_REGION: GZ_REGION, 
                ARG_UNTRANSLATED_TEXT: '『星詠み』'     # Option: 忽略不翻译的内容
            }
        )


    # 使用 tencent 翻译（专用接口）
    def test_tencent_trans_2(self) :
        client = TencentTranslation(
            api_id=self.TX_SECRET_ID, 
            api_key=self.TX_SECRET_KEY, 
            region=GZ_REGION             # Option: 选择最近自己位置的区域，可以加速接口网络
        )

        # 最少参数（写文件）
        result = client.translate(
            self.CONTENT, 
            from_lang='jp',
            to_lang='zh',
            savepath=self.TX_SAVE_PATH, 
            oncesave=True, 
            args={
                ARG_UNTRANSLATED_TEXT: '『星詠み』'     # Option: 忽略不翻译的内容
            }
        )

        # 最少参数（仅内存）
        result = client.translate(
            self.CONTENT, 
            from_lang='jp',
            to_lang='zh'
        )



    # 使用 ChatGPT 翻译（通用接口, 最全参数）
    def test_chatgpt_trans_1(self) :
        result = trans(
            self.CONTENT, 
            from_lang='日文',                   # Option: 通过指定 from_lang ，默认在内部生成 “翻译官” 的人设
            to_lang='中文',                     # Option: 通过指定 to_lang ，默认在内部生成 “翻译官” 的人设
            platform=CHATGPT, 
            api_id='', 
            api_key=self.GPT_API_KEY, 
            savepath=self.GPT_SAVE_PATH, 
            oncesave=False, 
            args={
                ARG_ROLE: self.GPT_AI_ROLE,     # Option: 直接定义人设，无需指定 from_lang 和 to_lang （内部生成的默认人设会被覆盖）
                ARG_OPENAI_MODEL: CHATGPT_35_TURBO, 
                ARG_PROXY_IP: '127.0.0.1', 
                ARG_PROXY_PORT: 8888
            }
        )


    # 使用 ChatGPT 翻译（专用接口）
    def test_chatgpt_trans_2(self) :
        client = ChatgptTranslation(
            self.GPT_API_KEY,
            openai_model=CHATGPT_35_TURBO,  # Option: 使用的模型，直接决定调用费用
            proxy_ip='127.0.0.1',           # Option: 国内需要挂代理
            proxy_port=8888                 # Option: 国内需要挂代理
        )

        # 最全参数
        result = client.translate(
            self.CONTENT, 
            savepath=self.GPT_SAVE_PATH, 
            oncesave=False, 
            from_lang='日文',                   # Option: 通过指定 from_lang ，默认在内部生成 “翻译官” 的人设
            to_lang='中文',                     # Option: 通过指定 to_lang ，默认在内部生成 “翻译官” 的人设
            args={
                ARG_ROLE: self.GPT_AI_ROLE,    # Option: 直接定义人设，无需指定 from_lang 和 to_lang （内部生成的默认人设会被覆盖）
            }
        )

        # 最少参数（写文件，默认人设）
        result = client.translate(
            self.CONTENT, 
            from_lang='日文',
            to_lang='中文',
            savepath=self.GPT_SAVE_PATH
        )

        # 最少参数（写文件，自定义人设）
        result = client.translate(
            self.CONTENT, 
            savepath=self.GPT_SAVE_PATH, 
            args={
                ARG_ROLE: self.GPT_AI_ROLE,
            }
        )

        # 最少参数（仅内存，默认人设）
        result = client.translate(
            self.CONTENT, 
            from_lang='日文',
            to_lang='中文'
        )

        # 最少参数（仅内存，自定义人设）
        result = client.translate(
            self.CONTENT, 
            args={
                ARG_ROLE: self.GPT_AI_ROLE,
            }
        )
        

if __name__ == '__main__':
    unittest.main()