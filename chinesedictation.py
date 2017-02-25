#!/usr/bin/python
#coding=utf-8
#author Minqi Zhou

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
def SubTitleBook(number,pdf):
	pdf.setFont('STSong-Light',14)
	#subTitle = "语文书第 " + str(number) + " 课 \n"
	subTitleStr = "语文书课文词语 \n"
	return subTitleStr

def SubTitleCard(number,pdf):
	pdf.setFont('STSong-Light',14)
	#subTitle = "语文卡片第 " + str(number) + " 课 \n"
	subTitleStr = "卡片词语 \n"
	return subTitleStr

def SubTitleError(number,pdf):
	pdf.setFont('STSong-Light',14)
	#subTitle = "语文错词第 " + str(number) +" 课\n"
	subTitleStr = "默写错误词语 \n"
	return subTitleStr

def SubTitleSentence(number,pdf):
	pdf.setFont('STSong-Light',14)
	subTitleStr = "默写课文句子 \n"
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

# compose a word line, which is a list, containing a set of pinyin of words
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

# generate all the pinyin for all words in the all lesson
def GenerateLessonPinyin(lesson):
	pinyinLesson = []
	for index in range(0,len(lesson)):
		pinyin = GenerateWordPinyin(lesson[index])
		pinyinWord = pinyin.split('-')
		pinyinWord = ProcessPolyPhonic(pinyinWord)
		pinyinLesson.append(pinyinWord)
	return pinyinLesson

# generate pinyin for a single word
def GenerateWordPinyin(word):
	from xpinyin import Pinyin
	p = Pinyin()
	pinyin =  p.get_pinyin(unicode(word),show_tone_marks=True)
	return pinyin

# decode pinyin: as for the polyphonic characters, we provided the pinyin code, for example zhe4, and we need to decode the code to original pinyin
def DecodePinyin(code):
	from xpinyin import Pinyin
	p = Pinyin()
	pinyin = p.decode_pinyin(code)
	return pinyin

# process the polyphonic characters in within a word or within a sentence
def ProcessPolyPhonic(sentence):
	word = 0           # starts from the first word
	while (word <  len(sentence)):
		if (sentence[word][0] == '('):
			polyPhonic =  DecodePinyin(sentence[word])
			sentence[word - 1] = polyPhonic
			del(sentence[word])
		word += 1

	return sentence

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

# draw words in one line on the canvas, which is drawn in the word by word manner
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

# draw a complete word line on the canvas, where the word line is composed first
def DrawLine(x,y,line,pdf):
	pdf.drawString(x,y,line)

# draw a line of grid on the canvas. the grid is the dianzi grid
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

# draw the pinyin on the canvas for words in an entire lesson
def DrawWordOneLesson(wordList,pdf):
	lessonWords = GenerateLessonPinyin(wordList)
	GenerateWords(lessonWords,pdf)

# draw the pinyin on the canvas for the sentences in an entire lesson
def DrawSentencesOneLesson(sentencesList,pdf):
	for sent in range(0,len(sentencesList)):
		sentence = sentencesList[sent]
		DrawOneSentence(sentence,pdf)

# draw the pinyin for a single sentence
def DrawOneSentence(sentence,pdf):
	global gPageCurrYPo
	global gPageCurrXPo
	global gPinyinHe
	global gGridHe
	global gBlankHe
	global gPageBottonPo

	currPos = 0
	sentenceWords = GenerateWordPinyin(sentence)
	wordList = sentenceWords.split('-')
	#wordList.append(words)
	wordList = ProcessPolyPhonic(wordList)

	while (currPos < len(wordList)):
		if (gPageCurrYPo < (gPageBottonPo + 50)):
			CreateNewPage(pdf)
		if ((len(wordList) - currPos) > 8):
			wordLine = [wordList[currPos:currPos+8]]
			currPos += 8
			
			pdf.setFont('pinyin',14)
			DrawWordLine(gPageCurrXPo,gPageCurrYPo,wordLine,pdf)
			gPageCurrYPo -= gPinyinHe
			DrawGrid(gPageCurrYPo,pdf)
			gPageCurrYPo -= gGridHe
			gPageCurrYPo -= gBlankHe
		else:
			wordLine = [wordList[currPos:len(wordList)]]
			
			pdf.setFont('pinyin',14)
			DrawWordLine(gPageCurrXPo,gPageCurrYPo,wordLine,pdf)
			gPageCurrYPo -= gPinyinHe
			DrawGrid(gPageCurrYPo,pdf)
			gPageCurrYPo -= gGridHe
			gPageCurrYPo -= gBlankHe
			
			currPos = len(wordList)



# draw the sub title within one lesson
def DrawSubTitle(title,pdf):
	global gPageCurrXPo
	global gPageCurrYPo
	pdf.drawString(gPageCurrXPo, gPageCurrYPo,title)
	gPageCurrYPo -= gLessonSubTitleHe

# create a new page in the pdf file
def CreateNewPage(pdf):
	global gPageCurrXPo
	global gPageCurrYPo
	global gPageLeftPo
	global gPageTopPo

	pdf.showPage()
	gPageCurrXPo = gPageLeftPo
	gPageCurrYPo = gPageTopPo

if __name__ == '__main__':
	
	lessons = [5]            # the lessions need to be generated, it is a array
	isBookIncluded = 1       # whether to generate words in the book or not 
	isCardIncluded = 1       # whether to generate words in the card or not
	isErrorWordsIncluded = 1 # whether to generate the words in the error list or not
	isSentencesIncluded = 1  # whether to generate the sentences in the book or not
	
	books = Books()
	bookChinese = books.bookChinese4       # select words in the fourth book in the elementary school
	title = books.lessonTitle4 
	sentencesChinese = books.bookSentence4 # select the sentences in the fourth book in the elementary school
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
			DrawSubTitle(SubTitleBook(lessons[less],f_word),f_word)
			#wordList = book[lessons[less] - 1]
			wordList = bookChinese[lessons[less] - 1]
			DrawWordOneLesson(wordList,f_word)
		if (isCardIncluded == 1):
			DrawSubTitle(SubTitleCard(lessons[less],f_word),f_word)
			#wordList = card[lessons[less] - 1]
			wordList = cardChinese[lessons[less] - 1]
			DrawWordOneLesson(wordList,f_word)
		if (isErrorWordsIncluded == 1):
			#wordList = error[lessons[less] - 1]
			wordList = errorChinese[lessons[less] - 1]
			if (len(wordList) != 0):
				DrawSubTitle(SubTitleError(lessons[less],f_word),f_word)
				DrawWordOneLesson(wordList,f_word)
		if (isSentencesIncluded == 1):
			sentencesList = sentencesChinese[lessons[less] - 1]
			if(len(sentencesList) != 0):
				DrawSubTitle(SubTitleSentence(lessons[less],f_word),f_word)
				DrawSentencesOneLesson(sentencesList,f_word)


		CreateNewPage(f_word)

	#f_word.showPage()
	f_word.save()
