#!/usr/bin/python
#coding=utf-8
import random
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# we use the A4 letter paper
# it's width is 595
# it's height is 841

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('pinyin','Pinyin.ttf'))

from Books import Books
from Cards import Cards
from Errors import Errors



#  generate the chinese pinying for dictation

# global variables
# setup the hight of the content on the A4 paper letter
gPageTopPo = 750        # the top position (y) of starting to print the content on each page
gPageBottonPo = 50      # the botton position (y) of ending to print the content on each page
gPageLeftPo = 50        # the left position (x) of starting to print the content on each page
gLessonTitleHe = 20     # the height of the lesson title
gLessonSubTitleHe = 20  # the height of the lesson sub title
gPinyinHe = 10          # the height of the pinyin line
gGridHe = 60            # the height of the grid
gBlankHe = 20           # the height of the filled in blank

# setup the variables to indicate the current position in the page
gPageCurrXPo = 0
gPageCurrYPo = 0

# setup the variables to control the words to be output within one lesson
gPosition = 0         # the position of the word sequence in generating the dication
gNextLesson = 0       # whether to generate the next lesson or not
gPageLine = 0         # the line number of the page
gWordsInLine = 8      # the maximum words that can be contained in one line

# -------------------------------------------------------------------------------------- #
# --------------------------------FUNCTIONS TO LAYOUT THE OUTPUT FILE------------------- #
# -------------------------------------------------------------------------------------- #
# write the entire title
def Title(number,pdf):
	global title
	pdf.setFont('STSong-Light',16)
	titleStr = "第 " + str(number) + " 课   " + title[number -1] + " \n"
	return titleStr

# generate the sub title for the sequence number of the specific lession
def SubBookTitle(number,pdf):
	pdf.setFont('STSong-Light',14)
	#subTitle = "语文书第 " + str(number) + " 课 \n"
	subTitleStr = "语文书课文词语 \n"
	return subTitleStr

def SubCardTitle(number,pdf):
	pdf.setFont('STSong-Light',14)
	#subTitle = "语文卡片第 " + str(number) + " 课 \n"
	subTitleStr = "卡片词语 \n"
	return subTitleStr

def SubErrorTitle(number,pdf):
	pdf.setFont('STSong-Light',14)
	#subTitle = "语文错词第 " + str(number) +" 课\n"
	subTitleStr = "默写错误词语 \n"
	return subTitleStr

def PrintGrid(file_handler):
	file_handler.write(" _______________________________________________________________________________\n")
	file_handler.write("|    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |\n")
	file_handler.write("|    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |\n")
	file_handler.write("|----¦----|----¦----|----¦----|----¦----|----¦----|----¦----|----¦----|----¦----|\n")
	file_handler.write("|    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |    ¦    |\n")
	file_handler.write("|____¦____|____¦____|____¦____|____¦____|____¦____|____¦____|____¦____|____¦____|\n")


# write a line to file f_word in terms of pinying in the given lesson 
# please note, that one line is able to accomendate 80 characteries
def LineComposition(lesson):
	# sequence number in generate the words
	lessonCharNo = len(lesson)
	cCharNoInWord = 0
	charNoInCC = 0
	blankNo = 0
	charNoInLine = 0

	global gPosition
	global gNextLesson
	global gPageLine
	# the output line which contains the line to print
	line = ''
	preLine = ''

	for word in range(gPosition,lessonCharNo):
		# add one word to the line
		preLine = line
		cCharNo = len(lesson[word])
		for char in range(0,cCharNo):
			charNoInCC = len(lesson[word][char])
			blankNo = 13 - charNoInCC
			for blank in range(0, (blankNo / 2)):
				line += ' '
			line += lesson[word][char]
			for blank in range(0, (blankNo / 2)):
				line += ' '
			charNoInLine += 1
			while (((len(line) - charNoInLine) % 13) != 0):
				line += ' '
		gPosition += 1
		# if the new added word exceed the length
		if ((len(line) - charNoInLine)>= 105 ):
			gPosition -= 1
			gPageLine += 1
			return preLine
		else:
			if ((len(line) - charNoInLine) > 91):
				break;
			for blank in range(1,13):
				line += ' '
			if (len(line) >= 105):
				break
	if (gPosition >= lessonCharNo ):
		gNextLesson = 1
	gPageLine += 1
	return line

def WordLineComposition(Lesson):
	global gPosition
	global gWordsInLine
	global gNextLesson

	wordsInLine = 0
	wordLine = []
	for word in range(gPosition, len(Lesson)):
		wordsInLine += len(Lesson[word])
		wordLine.append(Lesson[word])
		gPosition += 1
		if (wordsInLine == gWordsInLine):
			break
		elif(wordsInLine > gWordsInLine):
			gPosition -= 1
			wordLine = wordLine[:(len(wordLine) - 1)]
			break
		else:
			wordsInLine += 1
	if (gPosition == len(Lesson)):
		gNextLesson = 1
	return wordLine
			


# -------------------------------------------------------------------------------------------------------- #
# -----------------------GENERATE PINYIN FROM CHINESE WORDS ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------------- #
def GenerateLessonPinyin(lesson):
	pinyinLesson = []
	for index in range(0,len(lesson)):
		pinyin = GenerateWordPinyin(lesson[index])
		pinyinWord = pinyin.split('-')
		pinyinLesson.append(pinyinWord)
	return pinyinLesson

def GenerateWordPinyin(word):
	from xpinyin import Pinyin
	p = Pinyin()
	pinyin =  p.get_pinyin(unicode(word),show_tone_marks=True)
	return pinyin


# --------------------------------------------------------------------------------------------------------- #
# --------------------FUNCTIONS TO GENERATE THE WORDS IN LESSONS------------------------------------------- #
# --------------------------------------------------------------------------------------------------------- # 
def GenerateWords(lesson,pdf):
	pdf.setFont('pinyin',14)
	global gPosition
	global gNextLesson
	global gPageLine
	global gPageCurrYPo
	global gPageCurrXPo
	global gPageBottonPo

	while(gNextLesson == 0):
		if (gPageCurrYPo < (gPageBottonPo + 50)):
			CreateNewPage(pdf)
		#line = LineComposition(lesson)
		line = WordLineComposition(lesson)
		pdf.setFont('pinyin',14)
		#DrawLine(gPageCurrXPo,gPageCurrYPo,line,pdf)
		DrawWordLine(gPageCurrXPo,gPageCurrYPo,line,pdf)
		gPageCurrYPo -= gPinyinHe
		DrawGrid(gPageCurrYPo,pdf)
		gPageCurrYPo -= gGridHe
		gPageCurrYPo -= gBlankHe
	gNextLesson = 0
	gPosition = 0

def DrawWordLine(x,y,line,pdf):
	currentChar = 0
	pinyin = ''
	for word in range(0,len(line)):
		charNo = len(line[word])
		for char in range(0,charNo):
			charLen = len(line[word][char]) - 1
			for blank in range(0, (7-charLen)/2):
				pinyin += ' '
			pinyin += line[word][char]
			for blan in range(0,(7-charLen)/2):
				pinyin += ' '
			pdf.drawString(x + currentChar * 60, y, pinyin)
			currentChar += 1
			pinyin = ''
		currentChar += 1

def DrawLine(x,y,line,pdf):
	pdf.drawString(x,y,line)

def DrawGrid(startYPo, pdf):
	from reportlab.lib.colors import pink,black,red,blue,green
	pdf.setStrokeColor(pink)
	pdf.setDash(1,0)
	pdf.rect(50,startYPo,480,-60)
	for index in range(1,8):
		pdf.line(50 + index * 60,startYPo, 50 + index *60, startYPo -60)
	pdf.setDash(6,3)
	for index in range(0,8):
		pdf.line(50+30+index*60,startYPo,50+30+index*60,startYPo-60)
	pdf.line(50,startYPo-30,530,startYPo-30)

def CreateNewPage(pdf):
	global gPageCurrXPo
	global gPageCurrYPo
	global gPageLeftPo
	global gPageTopPo

	pdf.showPage()
	gPageCurrXPo = gPageLeftPo
	gPageCurrYPo = gPageTopPo

if __name__ == '__main__':
	
	lessons = [1,2,3,4]            # the lessions need to be generated, it is a array
	isBookIncluded = 1       # whether to generate words in the book or not 
	isCardIncluded = 1       # whether to generate words in the card or not
	isErrorWordsIncluded = 0 # whether to generate the words in the error list or not
	
	books = Books()
	bookChinese = books.bookChinese4       # select the fourth book in the elementary school
	title = books.lessonTitle4 
	cards = Cards()
	cardChinese = cards.cardChinese4       # select the fourth card in the elementary school
	errors = Errors() 
	errorChinese = errors.errorChinese4    # select the fourth error words in the elementary school

	line = ''
	f_word = canvas.Canvas('Dictation.pdf')
	f_word.setFont('STSong-Light',16)

	gPageCurrXPo = gPageLeftPo
	gPageCurrYPo = gPageTopPo

	for less in range(0,len(lessons)):
		f_word.drawString(200,gPageCurrYPo,Title(lessons[less],f_word))
		gPageCurrYPo -= gLessonTitleHe
		if (isBookIncluded == 1):
			f_word.drawString(gPageCurrXPo, gPageCurrYPo,SubBookTitle(lessons[less],f_word))
			gPageCurrYPo -= gLessonSubTitleHe
			#lesson = book[lessons[less] - 1]
			lesson = GenerateLessonPinyin(bookChinese[lessons[less] - 1])
			GenerateWords(lesson,f_word)
		if (isCardIncluded == 1):
			f_word.drawString(gPageCurrXPo,gPageCurrYPo,SubCardTitle(lessons[less],f_word))
			gPageCurrYPo -= gLessonSubTitleHe
			#lesson = card[lessons[less] - 1]
			lesson = GenerateLessonPinyin(cardChinese[lessons[less] - 1]) 
			GenerateWords(lesson,f_word)
		if (isErrorWordsIncluded == 1):
			f_word.drawString(gPageCurrXPo,gPageCurrYPo,SubErrorTitle(lessons[less],f_word))
			gPageCurrYPo -= gLessonSubTitleHe
			#lesson = error[lessons[less] - 1]
			lesson = GenerateLessonPinyin(errorChinese[lessons[less] - 1]) 
			GenerateWords(lesson,f_word)

		CreateNewPage(f_word)

	#f_word.showPage()
	f_word.save()
