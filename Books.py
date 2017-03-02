#!/usr/bin/python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# please notice that: as for the polyphonic characters, add the correct pinyin code righte after the chinese word
# 注意:对于多音字,请在中文字后加入正确的拼音编码
# example: "载(zai4)客", "记载(zai3)"  

class Books(object):
	lessonTitle4 = [
		       "太阳的话",         # lesson 1
			"享受森林",        # lesson 2
			"小黑鱼",          # lesson 3
			"沙滩上的童话",     # lesson 4
			"我的房间",         # lesson 5
			"马鸣加的新书包",    # lesson 6
			"海中救援",      # lesson 7
			"",      # lesson 8
			"",      # lesson 9
			"",      # lesson 10
			"",      # lesson 11
			"",      # lesson 12
			"",      # lesson 13
			"",      # lesson 14
			"",      # lesson 15
			"",      # lesson 16
			"",      # lesson 17
			"",      # lesson 18
			"",      # lesson 19
			"",      # lesson 20
			"",      # lesson 21
			"",      # lesson 22
			"",      # lesson 23
			"",      # lesson 24
			"",      # lesson 25
			"",      # lesson 26
			"",      # lesson 27
			"",      # lesson 28
			"",      # lesson 29
			"",      # lesson 30
			"",      # lesson 31
			"",      # lesson 32
			"",      # lesson 33
			"",      # lesson 34
			"",      # lesson 35
			"",      # lesson 36
			"",      # lesson 37
			"",      # lesson 38
			"",      # lesson 39
			"",      # lesson 40
               ]

	bookChinese4=[
			["花束", "香气","温暖","露水","枕头","睫毛","撒"], # lesson 1
			["享受", "森林","相信","杂草","繁密","枝丫","朝气蓬勃","凳子"], # lesson 2
			["快乐","金枪鱼","漆黑","充满","彩虹","果冻","清凉"],      # lesson 3
			["相约","建造","商量","驾驶","轰炸","赞赏"],      # lesson 4
			["功课","潜水艇","翅膀","墙壁","饼干","巧克力","司机","载","幻想"], # lesson 5
			["舅舅","婶婶","礼物","一股脑儿","班长(zhang3)","作业","羞愧难当","丝线"],   # lesson 6
			["救援","警报","营救","搏斗(dou4)","气喘吁(xu1)吁(xu1)","唯一","依靠"],      # lesson 7
			[],      # lesson 8
			[],      # lesson 9
			[],      # lesson 10
			[],      # lesson 11
			[],      # lesson 12
			[],      # lesson 13
			[],      # lesson 14
			[],      # lesson 15
			[],      # lesson 16
			[],      # lesson 17
			[],      # lesson 18
			[],      # lesson 19
			[],      # lesson 20
			[],      # lesson 21
			[],      # lesson 22
			[],      # lesson 23
			[],      # lesson 24
			[],      # lesson 25
			[],      # lesson 26
			[],      # lesson 27
			[],      # lesson 28
			[],      # lesson 29
			[],      # lesson 30
			[],      # lesson 31
			[],      # lesson 32
			[],      # lesson 33
			[],      # lesson 34
			[],      # lesson 35
			[],      # lesson 36
			[],      # lesson 37
			[],      # lesson 38
			[],      # lesson 39
			[],      # lesson 40
               ]

	bookHappyChinese4=[
			["春光明媚","细语","春回大地","徘徊","妙手回春","倾谈","冷冷清清","寂寞"],   # happy palace 1
			[],      # happy palace 2
			[],      # happy palace 2
			[],      # happy palace 2
		   ]
	bookSentence4 = [
  			 ["让我把花束,把香气,把晨曦,温暖和露水,撒满你们心的空间."],    # lesson 1
			 ["樱樱高兴极了,搬只凳子坐在树荫理,久久不肯离开."],    # lesson 2
			 ["它逃进漆黑的深水里,又孤独,又害怕."],    # lesson 3
			 ["于是,我们趴在沙滩上,从四面八方挖着(zhe4)地道."],    # lesson 4
			 ["在这里,我可以读书,可以幻想."],                # lesson 5
			 ["马鸣加羞愧难当,真想一头钻进书包里去."],         # lesson 6
			 ["我必须去.我们不能让那些留在海里的人无助地(de1)死去."],  # lesson 7
			 ["一个忘恩负义的人不会有朋友,更不会有好下场."], # lesson 8
			 ["由于他医术高明,前来就医的人总是络绎不绝."],   # lesson 9  
			 ["太阳一出来,数不清的蝴蝶在花丛间翩翩起舞."],   # lesson 10
			 ["西双版纳是植物的王国,又是动物的王国."],       # lesson 11
			 ["平静的湖面,犹如一面硕大的银镜."],            # lesson 12
			 ["啊!多好的阳光啊,我要把它带回去,作为礼物送给我的奶奶."], # lesson 13
			 ["只有第三个孩子接过妈妈手里沉甸甸的水桶,往前走."], #lesson 14
			 ["既然是老师的好学生,也应该是妈妈的好儿子."],      # lesson 15 
			 ["清凉的河水缓缓地流动,发出轻轻的潺潺声."],        # lesson 16
			 ["春风吹来,姹紫嫣红的花儿轻轻摇晃着,散发出阵阵芳香."],  # lesson 17
			 ["这样的成绩是假的,我才不要呢!"],       # lesson 18
 			 ["歌声给人们增添了勇气和力量,是歌声救了大家."] ,   # lesson 19
			 ["有一朵开着黄花,样子像尖瓣的莲花."],     # lesson 20
			 ["谁知手刚碰到铃铛,就被人发觉了."],     # lesson 21
			 ["尽管如此,它并不悲观失望,也不羡慕任何人."],     # lesson 22
			 ["微风把蒲公英妈妈的孩子送到四面八方."],     # lesson 23
			 ["我的心忐忑不安,真担心手里的碗像变戏法那样,突然间就碎了."],     # lesson 23
			 ["海龟用肚子当橡皮,把他辛辛苦苦写的诗全擦掉了."],     # lesson 25
			 ["一阵秋风吹过,那个玉米孤零零地站在那里,无奈地晃着脑袋."],     # lesson 26
			 ["教室里骤然间响起了掌声,那掌声热烈、持久."],     # lesson 27
			 ["一个人无论取得多大的成就,都不能自以为是."],     # lesson 28
			 ["我是苹果,一只小小的,红艳艳的苹果."],     # lesson 29
			 ["别人无论问什么,牧童都能给出一个聪明的回答,因而远近闻名."],     # lesson 30
			 ["这头象又高又大,身子像堵墙,腿像四根柱子."],     # lesson 31
			 ["这树挂满了墨绿色的叶子,就像一把巨大的伞."],    # lesson 32
			 ["骆驼啃过的树叶上留下了牙齿印,所以知道它缺了一颗牙齿."],     # lesson 33
			 ["乐声表露出的思乡之情,深深地打动了大家."],     # lesson 34
			 ["母山羊快速溜出山洞,逃出了狮子的爪牙."],     # lesson 35
			 ["没有熟透的杨梅又酸又甜,熟透了就甜津津的,叫人越吃越爱吃."],     # lesson 36
			 ["花儿可漂亮呢,就像一个个小喇叭,有紫红的,有蓝的,有白的."],     # lesson 37
			 ["飞到河边上,小鱼在做梦；飞到树林里,小鸟睡正浓."],     # lesson 38
			 ["远远望去,一只只鸬鹚又像士兵似的,整齐地站在船舷上."],     # lesson 39
			 ["喜鹊体态优美,鸣声清脆,又能帮助人们消灭害虫,人们怎能不喜欢它呢?"],     # lesson 40
                    ]


