#!/usr/bin/python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# please notice that: as for the polyphonic characters, add the correct pinyin code righte after the chinese word
# 注意:对于多音字,请在中文字后加入正确的拼音编码
# example: "载(zai4)客", "记载(zai3)" 

class Errors(object):
	errorChinese4 = [
				[],  # lesson 1				
				["捆绑","铺天盖地"],  #lesson 2
				["充满"],  #lesson 3
				["腾云驾雾","挖洞","插花"], # lesson 4
				[],                         # lesson 4
			]
	errorChineseExam4 = [
 				["昂首怒放","武器"], # 周练 1
	
			    ]

