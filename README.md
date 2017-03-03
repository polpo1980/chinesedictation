#Welcome to Chinese Dictation


Generate the Chinese Dictation form from the given Chinese words.

* Input chinese words in the book into Books.py
* Input chinese words in the word card into Cards.py
* Input error chinese words into Errors.py


How to generate the PDF which contains the dictation form

python chinesedictation.py

Known Bugs
* It is unable to hundle the polyphonic characters right now
* fix add the specific pinyin after the polyphonic characters, i.e., 着(zhe1)



如何使用:

为了节省编码时间,没有制作界面.大家可以按照如下方式再生成所需要的拼音默写.
1. 安装Reportlab第三方库,用于生成pdf文件
* Windows系统安装,请参考.https://zhidao.baidu.com/question/1670112558921372067.html
* Mac系统安装, 使用命令,sudo easy_install reportlab
* Redhat 系列Linux系统安装,使用命令,sudo pip install reportlab

2. 填写课文词语
* 在Books.py中填入对应位置填入词语
* 在Cards.py中填入对应的卡片词语
* 在Errors.py中填入默写错误的词语

3. 修改需要生成的课文词语
* 在chinesedictation.py 的350行修改需要生成的课文.比如需要生成1-4课,则写入1,2,3,4

4. 生成拼音pdf
运行chinesedictation.py,就可以得到相应的默写文件


