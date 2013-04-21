#
# This file is based on a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher modified 2013 Jarrod Cary
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

try:
  import pkg_resources
	pkg_resources.require("dragonfly >= 0.6.5")
except ImportError:
	pass
from natlink import displayText
from dragonfly import *
from htmlTags import *
from _namingcon import *
import sys

release = Key("shift:up, ctrl:up")
locationNum=False

def charsLastUtterance(tagN):
	#bob = tagN
	numChars = (len("%s" % tagN) + 2)
	#print numChars
	Key("left:%s" % numChars).execute()

def tagFormat(tagN):
	# Callback when tagN is spoken.
	textToPrint = tagN
	someString = str(textToPrint)
	String = someString.lower()
	printer = Text(String.replace(' ', ''))
	printer.execute()

def stuffFormat(stuff):   
	# Callback when stuff is spoken.
	someString = str(stuff)
	lowerString = someString.lower()
	words = lowerString.split()
	finalString = ""
	isFirst = 1
	for word in words:
		if isFirst == 1:
			finalString = finalString + word
			isFirst = 0
		else:
			finalString = finalString + word.title()
	printer = Text(finalString)
	printer.execute()

def colorAlpha(alpha, color):
	rtn1 = len(color) + 2          
	rtn2 = len(color) + 1
	if color != "":
		Text("rgb(%s)" % color).execute()
	if alpha != "":
		printer = Key("left:%s" % rtn1) + Text("a") + Key("right:%s" % rtn2) + Text(",%s" % alpha) + Key("right")
		printer.execute()

def cssScope(stopHere):
	n = 1
	original = Clipboard(from_system=True)
	def checker():
		global new
		(Key("end, shift:down, left, shift:up, c-c, end") + Pause("10")).execute()
		new = Clipboard(from_system=True)
	while n >= 1:
		if n > 0:
			checker()
			if stopHere == "{" and n > 0: #up
				Key("up, end").execute()
				n = 2
			if stopHere == "}" and n > 0: #down
				Key("down, end").execute()
				n = 2
			if new.get_text() == stopHere:
				n = 0
			if n == 0: 
				original.copy_to_system()

def htmlScope(direction, type, select=False, select2=False):
	counter = 0
	def directionCheck():
		global new
		if direction == "right":
			(Key("shift:down, right, shift:up, c-c, right") + Pause("2")).execute()
		if direction == "left":
			(Key("shift:down, left, shift:up, c-c, left") + Pause("2")).execute()
		new = Clipboard(from_system=True)
	n = -1
	if n == -1:
		if direction == "right" and type == "closer" and select == False:
			(Pause("1") +Key("right:2")).execute()
		if direction == "left" and type == "opener":
			if select2 == False:
				(Pause("1") + Key("left")).execute()
			if select2 == True:
				(Pause("1") + Key("right")).execute()
		n = 1
	catch = 0
	original = Clipboard(from_system=True)
	while n >= 0:
		catch += 1
		if catch > 2500:
			print "Went too long without a match"
			break
		if n > 0:
			if direction == "right" and type == "closer":
				counter += 1
			directionCheck()
			if ((new.get_text() =="<" and n == 1 and direction == "right") or (new.get_text() =="/" and n == 1 and direction == "left") and type == "closer") or ((new.get_text() =="<" and n == 1 and direction == "right") or (new.get_text() ==">" and n == 1 and direction == "left") and type == "opener"):
				if type == "closer":
					n = 2 # sound first matching character
				if type == "opener":
					n = 4 # continue moving through the tag until you find the other side
					counter += 1
				(Pause("1")).execute()
				directionCheck()
				if new.get_text() == "/" and type == "opener":
					n = 1
			if ((new.get_text() =="/" and n == 2 and direction == "right") or (new.get_text() =="<" and n == 2 and direction == "left") and type == "closer") or ((new.get_text() ==">" and n == 4 and direction == "right") or (new.get_text() =="<" and n == 4 and direction == "left") and type == "opener"):
				n = 3 # found second matching character
				if new.get_text() == "/" and type == "opener":
					n = 2
			if ((new.get_text() =="/" and n == 3 and direction == "right") or (( new.get_text() =="<" ) and ( n == 3 ) and ( direction == "left" )) and type == "closer") or ((new.get_text() ==">" and n == 3 and direction == "right") or (new.get_text() =="<" and n == 3 and direction == "left") and type == "opener"):
				n = 0 # relevant string found
			if ((new.get_text() !="/" and n == 2 and direction == "right") or (new.get_text() !="<" and n == 2 and direction == "left") and type == "closer") or ((new.get_text() !=">" and n == 4 and direction == "right") or (new.get_text() !="<" and n == 4 and direction == "left") and type == "opener"):	
				if type == "closer":
					n = 1
				if type == "opener":
					counter += 1
					n = 4
					if new.get_text() == "/":
						n = 1
						counter = 0
			if n == 0: # stop searching
				original.copy_to_system()
				if direction == "right" and type == "closer":
					(Key("left:2")).execute()
					if select == True:
						print counter
						(Key("shift:down, left:%s, shift:up" % (counter -1))).execute()
				if direction == "left" and type == "opener":
					Key("right:%s" % (counter + 1)).execute()
				break

def selectContents():
	global between
	htmlScope("left", "opener", select2=True)
	(Pause("1") + Key("")).execute()
	htmlScope("right", "closer", select=True)

def attribute():
	htmlScope("left", "opener")

def attributeEsc():
	htmlScope("left", "opener")
	htmlScope("right", "opener")

def listAttributes():
	d = []
	print "\n<ATTRIBUTES>\n"
	for key, value in sorted(tagsAttribute.iteritems(), key=lambda joe: joe[0].lower()):
		a = len(key)
		b = ""
		c = 25 - a
		while c > 0:
			b = b + "."
			c -= 1
		e = ('"' + key.upper() + '"' + b + "-| " + value + ":")
		d.append(e)
		v ='\n'.join(d)
	print v
	print "\n</ATTRIBUTES>\n"
	global variable

def listTags():
	natlink.displayText("hello",0)
	print "\n<HMTL TAGS>\n"
	for key, value in sorted(htmlTags.iteritems(), key=lambda joe: joe[0].lower()):
		a = len(key)
		b = ""
		c = 26 - a
		while c > 0:
			b = b + "."
			c -= 1
		print '"' + key.upper() + '"' + b + "-| <" + value + ">"
	print "\n</HTML TAGS>\n"

def cssProp(browserPrefix,cssTagPrefix,cssTag,cssTagSuffix):
	printer = browserPrefix+cssTagPrefix+cssTag+cssTagSuffix
	(Text("%s:;" % printer) + Key("left")).execute()
	print len(printer)

def cssPropList(cssTagsList):
	printer = cssTagsList
	(Text("%s:;" % printer) + Key("left")).execute()

def listCSSProps():
	print "\n<Available CSS Properties>\n"
	for key, value in sorted(tagsCSSlist.iteritems(), key=lambda joe: joe[0].lower()):
		a = len(key)
		b = ""
		c = 26 - a
		while c > 0:
			b = b + "."
			c -= 1
		print '"' + key.upper() + '"' + b + "-| " + value + ":"
	print "\n</Available CSS Properties>\n"

def rememberPos():
	'''grabs all text from your current cursor position to the beginning of the document'''
	#global locationNum
	location = []
	(Pause("5") + Key("cs-home, c-c") + Pause("5")).execute()
	lineClip = Clipboard(from_system=True)
	#print countClip.get_text() + "\n"
	for charlist in lineClip.get_text():
		if charlist != "\n":
			location.append(charlist)
	return len(location)

def ReturnPrev():
	if locationNum:
		#(Key("c-home, right:%s" % locationNum)).execute()
		#Key("c-home, down:%s" % locationNum[1]).execute()
		Key("c-home, right:%s" % locationNum).execute()
	else:
		print "error: location not set"

def fooBar(type, tagN, direction):
	global locationNum
	aa = locationNum
	magic = []
	t = rememberPos()
	magic.append(t)
	h = HTMLParser(0, 0, type, tagN, direction)
	#print t
	print h[0]
	if tagN != "":
		for i in range(len(h[0])):
			if type == "closer":
				if h[0][i][2] == "end":
					magic.append(h[0][i][0])
				print t, h[0][i][0]
			if type == "opener":
				if h[0][i][2] == "start":
					magic.append(h[0][i][1])
				print t, h[0][i][1]
	else:
		for i in range(len(h[0])):
			if h[0][i][2] == "end":
				magic.append(h[0][i][0])
			if h[0][i][2] == "start":
				magic.append(h[0][i][1])

	magic.sort()
	print magic
	for i in range(len(magic)):
		if magic[i] == t and direction == "right":
			locationNum = magic[i+1]
		if magic[i] == t and direction == "left":
			locationNum = magic[i-1]
	ReturnPrev()
	locationNum = aa
	print type, tagN, direction

def HTMLParser(n, position, type, tagN, direction):
	#print n, position, type, tagN, direction
	print "\n*******************************BEGIN*******************************"
	'''Parse HTML from clipboard, returns a list containing two ints and three strings.
        HTMLParser(n=0, position=0, type, tagN, direction):
        HTMLParser(7, (0 or 1), "opener/closer/comment/doctype", "div/a/img/etc", "left or right"):
        '''
	originalClipboard = Clipboard(from_system=True)
	stack = []
	tag = []
	t = 0
	ot = ""
	ida = -1
	yo = []
	k = -1
	global locationNum
	locationNum = rememberPos()
	# copies every character from your file into its own place in a list
	(Pause("1") + Key("c-a, c-c") + Pause("1")).execute()
	newClip = Clipboard(from_system=True)
	stacklines = 0
	for c in newClip.get_text():
		if c == "\n":
			stacklines += 1
		if c != "\n":
			stack.append(c)
	for i in range(((len(stack)))):
		if stack[i] == "<":
			start = i
			if stack[i+1] == "/":
				inside = 2
				ot = "end"
			elif stack[i+1] == "!":
				inside = 2
				ot = "doctype"
			else:
				inside = 1
				ot = "start"
		if stack[i] == ">" and ot != "":
			kind = ot
			ot=""
			stop = i + 1

			tag.append([start, stop, kind, ida]) #tagN added later, calculated from (start, stop)
	def tagName(num):
		tagStr = []
		for i in range(tag[num][0], tag[num][1]):
			tagStr.append(stack[i])
			Tag = "".join(tagStr)
		return Tag
	countOpen=0
	countClose=0
	ida = 0
	boogie = 0
	for i in range(len(tag)):
		iTag = tagName(i)# [0] = 1st word
		n1 = iTag.split()[0] #failsafe <whole-tag-un-sliced>
		n2 = iTag.split()[0][1:] #one off start <tagname param
		n3 = iTag.split()[0][2:-1] #two off start, one off end </ >
		n4 = iTag.split()[0][1:-1] # one off start, one off end < >
		nFirst = iTag.split()[0][0:1:] #first
		nSecond = iTag.split()[0][1:2:] #second
		nLast = iTag.split()[0][-1::] #last
		
		if nFirst == "<" and nSecond != "/" and nLast == ">":
			insideOpener = n4
		elif nFirst == "<" and nSecond == "/" and nLast == ">":
			insideOpener = n3
		elif nFirst == "<" and nSecond != "/" and nLast != ">":
			insideOpener = n2
		else:
			insideOpener = n1
		tag[i].append(insideOpener)
		if tag[i][2] == "start":
			ida +=1
			tag[i][3] = ida
		#print "\n",i, ":", tag[i]

		for j in range(i):
			if tag[i][4] == tag[j][4] and tag[i][2] != tag[j][2] and tag[j][2] != "startTemp":
				if tag[i][3] == -1:
					k = j
					#print "\t",tag[j], j
					#
		#print "\t\t",k, ":", tag[k]
		#tag[i][3] = tag[k][3]
		if tag[k][2] == "start":
			tag[k][2] = "startTemp"
		#
			tag[i][3] = tag[k][3]
			
			#print tag[j][4]
		#print tag[i][0:2], tag[i][2], tag[i][4], "   boogie:", boogie			#print "J2: %s ::" %j, tag[j][0:2], tag[j][2], tag[j][4], boogie
					
				#print woogie, "\n______________", boogie
					

		if tag[i][4] == "!--":
			tag[i][2] = "comment"
		if tag[i][4] == tagN:
			print tag[i]
			yo.append(tag[i])
	for i in range(len(tag)):
		if tag[i][2] == "startTemp":
			tag[i][2] = "start"
	print "i %s" % i
	#print (n1,n2,n3,n4,n5,n6,n7)
	print "tag: %s" % tag[n]
	print "********************************END********************************"
	if tag[n][2] == "start" and position != 0:
		position = 1
	elif tag[n][2] == "end" and position == 0:
		position = 0
	else:
		pass
	keysA = (tag[n][position])
	print keysA
	print "locationNum: %s" % locationNum
	print "Tag: ",tag,"\n"
	(Pause("4") + (Key("c-home, right:%s" % keysA) + Pause("4"))).execute()
	originalClipboard.copy_to_system()
	if tagN:
		return yo, tag, position
	return tag[n], tag, position

def reload():
	unload()
###########################################################################

# configuration for KeystrokeRule
config = Config("html edit")
config.cmd = Section("Language section")
config.cmd.extra = Item([
	IntegerRef("n", 0, 100, default =0),
	Dictation("text"),
	Dictation("text2"),
	Dictation("stuff", default=""), 
	Dictation("command"),
	Choice("cssTagsList", tagsCSSlist, default=""),
	Choice("cssTag", tagsCss, default = ""), 
	Choice("cssTagPrefix", tagsCssPrefix, default = ""), 
	Choice("cssTagSuffix", tagsCssSuffix, default = ""), 
	Choice("browserPrefix", tagsBrowserPrefix, default = ""),
	Choice("alpha", tagsAlpha, default = ""), 
	Choice("color", tagsColor, default = ""),
	Choice("attribute", tagsAttribute, default = ""),
	Choice("target", tagsTarget, default = ""),
	Choice("tagN", htmlTags, default = ""),
	Choice("and", {"and":", "}, default = " "),
	
	Choice("direction", {
		"(previous | left)"     :"left",
		"(next | right)"        :"right",}, default = "right"),
	Choice("type", {
		"closer"                :"closer",
		"opener"                :"opener",}, default = "opener"),
		Choice("position",{
		"beginning"             :0,
		"end"                   :1,
		}, default=0),
	Choice("stopHere", {
		"up"                    :"{",
		"down"                  :"}",}, default = "{"),
	Integer("value", 0, 800),
		#Integer("n", 0, 20, default=0),
	])
config.cmd.map =  Item(
	{
	 #html
	"<tagN> tag":# creates a pair of HTML tags and moves the cursor between them
		Text("<></>") + Key("left:4") + Function(tagFormat) + Key("right:3") + Function(tagFormat) + Function(charsLastUtterance),
	"<tagN> opener":#  creates an opener of an HTML tag
		Text("<>") + Key("left") + Function(tagFormat) + Key("right"),
	"<tagN> closer":#  creates a culture of an HTML tag
		Text("</>") + Key("left") + Function(tagFormat) + Key("right"),
	"make solo tag":#  converts in opener HTML tag into a one-off XHTML type tag
		Key("left:1") + Text(" /") + Key("right"),
	"attribute <attribute> [<color>][<stuff>][alpha <alpha>][<target>]":
		Key("right") + Function(attribute) + Key("left") + Text( ' %(attribute)s=""') + Key("left") + Function(stuffFormat) + Function(colorAlpha) + Text("%(target)s") + Function(attributeEsc),
	"list attributes":# just available HTML attributes in the Python console
		Function(listAttributes),
	"list tags":	#  list available HTML tag in Python console
		Function(listTags),
	"insert color <color> [alpha <alpha>]":	# insert an RGB color with optional Alpha attribute
		Function(colorAlpha),
	"end of next line":
		Key("end, down, end"),
	"new html template":	# basic HTML page wrapper
		Text("<html>\n\n<head>\n<title></title>\n<meta></meta>\n</head>\n\n<body></body>\n\n</html>") + Key("home, up:9"),
	"go to <direction> [<type>] tag":	# direction being either previous or next and type being opener or closer <opener>*</ closer>
		Function(htmlScope),
		#Function(HTMLParser),
	"select contents": # select the text between an open or closer tag
		Function(selectContents),
	"parse [<type>] tag [<n>][at <position>][<tagN>]":
		Function(HTMLParser),
	"return to remembered":
		Function(ReturnPrev),
	"foo bar":Function(fooBar),
	"floop <direction> [<tagN>] <type>":Function(fooBar),
	#css
	"exit block <stopHere>"    : Function(cssScope),
	"<value> (pixels | pixel)" : Text("%(value)dpx"),
	"<value> (points | point)" : Text("%(value)dpt"),
	"list prop <cssTagsList>"  : Function(cssPropList),
	"css comment"              : Text("/*  */") + Key("left:3"),
	"ID select <stuff>": # Creates a new ID Selector
		Text("#") + Function(stuffFormat) + Text(" {\n\n}") + Key("up"),
	"class select <stuff>": # Creates a New Class Selector
		Text(".") + Function(stuffFormat) + Text(" {\n\n}") + Key("up"),
	"tag select <tagN>": # creates a new tag selector
		Function(tagFormat) + Text(" {\n\n}") + Key("up"),
	"[<and>] tag add <tagN>": # adds an additional tag selector
		Function(cssScope) + Key("left:2,") + Text("%(and)s") + Function(tagFormat) + Key("down, end"),
	"[<and>] class add <stuff>": # adds an additional class selector
		Function(cssScope) + Key("left:2,") + Text("%(and)s.") + Function(stuffFormat) + Key("down, end"),
	"[<and>] ID add <stuff>": # adds an additional ID selector
		Function(cssScope) + Key("left:2,") + Text("%(and)s#") + Function(stuffFormat) + Key("down, end"),
	"css prop [<browserPrefix>] [<cssTagPrefix>] <cssTag> [<cssTagSuffix>]":
		Function(cssProp),
	"list css properties":# just available Css properties in the Python console
		Function(listCSSProps),
		
	"reload html grammar":Function(reload),
	},
	namespace={
		"Key"              : Key,
		"Text"             : Text,
		"Function"         : Function,
		}
	)
config.load()

###########################################################################

class HTMLEnabler(CompoundRule):# disable bootstrap, enable HTML grammar.
	spec = "Enable HTML"                  # Spoken form of command.
	def _process_recognition(self, node, extras):   # Callback when command is spoken.
		HTMLBootstrap.disable()
		grammar.enable()
		print "HTML grammar enabled"

class HTMLDisabler(CompoundRule):# disable HTML grammar enable bootstrap
	spec = "switch language"
	def _process_recognition(self, node, extras):
		grammar.disable()
		HTMLBootstrap.enable()
		print "HTML grammar disabled"

class KeystrokeRule(MappingRule):
	exported                = False
	mapping                 = config.cmd.map
	extras                  = config.cmd.extra
	defaults                = {"n": 1,}

# Alternative(children=(), name=None, default=None)
# RuleRef(rule, name=None, default=None)
# Repetition(child, min=1, max=None, name=None, default=None)
#sequence = Repetition(Alternative(children=[RuleRef(rule=KeystrokeRule())]), min=1, max=16, name="sequence")
class RepeatRule(CompoundRule):
	spec = "<sequence> [[[and] repeat [that]] <n> times]" 
	extras = [
		#sequence,
		Repetition(Alternative(children=[RuleRef(rule=KeystrokeRule())]), min=1, max=16, name="sequence"),
		IntegerRef("n", 1, 100),# Times to repeat the sequence.
		]
	defaults = {"n": 1,}
	def _process_recognition(self, node, extras):
		print "beginning sequence recognition"
		sequence = extras["sequence"]   # A sequence of actions.
		count = extras["n"]# An integer repeat count.
		for i in range(count):
			for action in sequence:
				action.execute()
		release.execute()
		print "end sequence recognition"

###########################################################################


HTMLBootstrap = Grammar("HTML bootstrap")# Create a grammar to contain the command rule.
grammar = Grammar("html edit")   # Create this module's grammar.
HTMLBootstrap.add_rule(HTMLEnabler())
HTMLBootstrap.load()
grammar.add_rule(HTMLDisabler())
grammar.add_rule(RepeatRule())    # Add the top-level rule.
grammar.load()# Load the grammar.


def unload():
	global grammar
	if grammar: grammar.unload()
	grammar = None
