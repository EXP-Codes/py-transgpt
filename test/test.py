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


class TestScenes(unittest.TestCase):

    @classmethod
    def setUpClass(cls) :
        pass


    @classmethod
    def tearDownClass(cls) :
        pass


    def setUp(self) :
        self.content = '''
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


    def test_baidu_trans(self) :
        result = trans(
            self.content, 
            from_lang='jp', 
            to_lang='zh', 
            platform=BAIDU, 
            api_id='xxxxxxxxxxxxxxxx', 
            api_key='yyyyyyyyyyyyyyyy', 
            savepath='./test/output/result_baidu.txt'
        )


    def test_tencent_trans(self) :
        result = trans(
            self.content, 
            from_lang='jp', 
            to_lang='zh', 
            platform=TENCENT, 
            api_id='xxxxxxxxxxxxxxxx', 
            api_key='yyyyyyyyyyyyyyyy', 
            savepath='./test/output/result_tencent.txt', 
            args={
                ARG_REGION: GZ_REGION, 
                ARG_UNTRANSLATED_TEXT: '『星詠み』'
            }
        )


    def test_chatgpt_trans(self) :
        result = trans(
            self.content, 
            from_lang='日文',
            to_lang='中文',
            platform=CHATGPT, 
            api_id='', 
            api_key='sk-xxxxxxxxxxxxxxxx', 
            savepath='./test/output/result_chatgpt.txt', 
            args={
                ARG_ROLE: '基于《从零开始的异世界生活》小说的背景，把日文内容翻译成中文，并润色',
                ARG_OPENAI_MODEL: CHATGPT_35_TURBO, 
                ARG_PROXY_IP: '127.0.0.1', 
                ARG_PROXY_PORT: 8888
            }
        )


if __name__ == '__main__':
    unittest.main()