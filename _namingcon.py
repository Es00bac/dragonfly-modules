from dragonfly import *

def copyLn(n, direction):
  n = n + 1
	originalClipboard = Clipboard(from_system=True)
	text = originalClipboard.get_text()
	while n > -1 and direction == "down":
		if n > 0:
			(Key("home, shift:down, end, shift:up, c-c, end") + Pause("1")).execute()
		if n > 1:
			Key("end, enter, end, c-v").execute()
		if n < 1:
			originalClipboard.copy_to_system()
		n = n - 1
	while n > -1 and direction == "up":
		if n > 0:
			(Key("home, shift:down, end, shift:up, c-c, end") + Pause("1")).execute()
		if n > 1:
			Key("home, enter, up, c-v").execute()
		if n < 1:
			originalClipboard.copy_to_system()
		n = n - 1

# helper function handling "camelBack"
def camel_back(command):
	someString = str(command)
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

# Voice command rule for "Camel" naming convention.
def camel_format(command):	# Callback when command is spoken.
	textToPrint = command
	someString = str(textToPrint)
	upperString = someString.title()
	printer = Text(upperString.replace(' ', ''))
	printer.execute()

# Voice command rule for "middle_underscores" naming convention.
def middle_underscores(command):	# Callback when command is spoken.
	textToPrint = command
	someString = str(textToPrint)
	printer = Text(someString.replace(' ', '_'))
	printer.execute()

# Voice command rule for "_BEGINNING_UNDERSCORES" naming convention.
def _BEGINNING_UNDERSCORES(command):	# Callback when command is spoken.
	textToPrint = command
	someString = str(textToPrint)
	upperString = "_" + someString.upper()
	printer = Text(upperString.replace(' ', '_'))
	printer.execute()            

# Voice command rule for "middle-slash" naming convention.
def middle_slash_format(command):	# Callback when command is spoken.
	textToPrint = command
	someString = str(textToPrint)
	printer = Text(someString.replace(' ', '-'))
	printer.execute()

# Voice command rule for "spacefree" naming convention.
def SpaceFreeFormat(command):	# Callback when command is spoken.
	textToPrint = command
	someString = str(textToPrint)
	printer = Text(someString.replace(' ', ''))
	printer.execute() 

def SpaceFormat(text):	# Callback when command is spoken.
	textToPrint = text
	someString = str(textToPrint)
	printer = Text(someString)
	printer.execute() 



class cursorManipulator(MappingRule):
	mapping = {
		"shapow"                : Key("end, enter"),
		"whapow"                : Key("home, enter, up"),
		"kapow"                 : Key("down, end, enter:2"),
		}

class ProgrammingNamingConventions(MappingRule):
	mapping  = {
		#both of these commands do the same thing in terms of name formatting   example: testValue
		"var <command>":

		  Function(camel_back),
		"var <command> <symbol>":
		  Function(camel_back) + Text("%(symbol)s"),
		  "<symbol> var <command>":
		  Text("%(symbol)s") + Function(camel_back),
				
		  "camelback <command>":
		  Function(camel_back),
		  "camelback <command> <symbol>":
		  Function(camel_back) + Text("%(symbol)s"),
		  "<symbol> camelback <command>":
		  Text("%(symbol)s") + Function(camel_back),

		  #this command capitalizes the 1st letter of each word and removes spaces   example: TestValue
		  "camel <command>":
		  Function(camel_format),
		  "camel <command> <symbol>":
		  Function(camel_format) + Text("%(symbol)s"),
		  "<symbol> camel <command>":
		  Text("%(symbol)s") + Function(camel_format),

		  #this command replaces spaces between words with underscores  example:test_value
		  "middle under <command>":
		  Function(middle_underscores),
		  "middle under <command> <symbol>":             Function(middle_underscores) + Text("%(symbol)s"),
		  "<symbol> middle under <command>":              Text("%(symbol)s") + Function(middle_underscores),

		  #example of this command: _TEST_VALUE
		  "beginning under <command>":
		  Function(_BEGINNING_UNDERSCORES),
		  "beginning under <command> <symbol>":
		  Function(_BEGINNING_UNDERSCORES) + Text("%(symbol)s"),
		  "<symbol> beginning under <command>":
		  Text("%(symbol)s") + Function(_BEGINNING_UNDERSCORES),

		  #example of this command: test-value
		  "middle lines <command>":
		  Function(middle_slash_format),
		  "middle lines <command> <symbol>":
		  
		  Function(middle_slash_format) + Text("%(symbol)s"),
		  "<symbol> middle lines <command>":
		  Text("%(symbol)s") + Function(middle_slash_format),

		  # example of this command: testvalue                
		  "space free <command>":
		  Function(SpaceFreeFormat),
		  "space free <command> <symbol>":
		  Function(SpaceFreeFormat) + Text("%(symbol)s"),
		  "<symbol> space free <command>":
		  Text("%(symbol)s") + Function(SpaceFreeFormat),
	   }

	extras   = [
		Dictation("command"),
		Choice("symbol",{
			"dot":".",
			"arrow":"->",
			"parameters":"()",
			"parameters dot":"()."
			}, default="")
		] 

class DataComparisons(MappingRule):
	mapping = {
			"equal to":
			Text(" = "),
			"absolute equal to":
			Text(" == "),
			"addition":
			Text(" + "),
			"subtraction":
			Text(" - "),
			"multiplication":
			Text(" = "),
			"division":
			Text(" / "),
			"greater than":
			Text(" > "),
			"less than":
			Text(" < "),
		}
class bracketTypes(MappingRule):
	mapping = {
		 "curly brackets":
		 Text("{}") + Key("left:1"),
		 "round brackets":
		 Text("()") + Key("left:1"),
		 "square brackets":
		 Text("[]") + Key("left:1"),
		 "angle brackets":
		 Text("<>") + Key("left:1"),
	}
class betterCopy(MappingRule):

	mapping = {
				"better copy":
				Key("c-z"),
				"better paste":
				Key("c-v"),
				"better cut":
				Key("c-x"),
	}

class pythonCoolShit(MappingRule):
	#def speakChar(string):
		
	def lineDeleter(n, direction):
		while n > 0 and direction == "up":
			if n > 0:
				(Key("up, end, shift:down, home:2, shift:up, delete") + Pause("10")).execute()
			n = n - 1
		while n > 0 and direction == "down":
			if n > 0:
				(Key("down, end, shift:down, home:2, shift:up, delete") + Pause("10")).execute()
			n = n - 1
	def copyLn(n, direction):
		n = n + 1
		originalClipboard = Clipboard(from_system=True)
		text = originalClipboard.get_text()
		while n > -1 and direction == "down":
			if n > 0:
				(Key("home, shift:down, end, shift:up, c-c, end") + Pause("1")).execute()
			if n > 1:Key("end, enter, end, c-v").execute()
			if n < 1:
				originalClipboard.copy_to_system()
			n = n - 1
		while n > -1 and direction == "up":
			if n > 0:
				(Key("home, shift:down, end, shift:up, c-c, end") + Pause("1")).execute()
			if n > 1:
				Key("home, enter, up, c-v").execute()
			if n < 1:
				originalClipboard.copy_to_system()
			n = n - 1
	def c_z(n):
		while n + 1 > 0:
			(Pause("20") + Key("c-z")).execute()
			n = n - 1

	def columnMaker(symbol = "=", margin=25, found = False):
		originalClipboard = Clipboard(from_system=True)
		(Key("end, shift:down, home, shift:up, c-c") + Pause("1")).execute()
		newClip = Clipboard(from_system=True)
		#originalClipboard.copy_to_system()
		i = 0
		for c in newClip.get_text():
			i += 1
			if c == symbol and found == False:
				found = True
				print c, i
				spaces = margin - i
				print margin
				action = (Key("left, right:%s" % (i -1)) + Key("space:%s, end" % spaces))
				action.execute()
				print action
		originalClipboard.copy_to_system()

	def lineNumbers(aa,ab,ac,ad):
		number = []
		if aa != 0:
			number.append(aa)
			if ab != 0:
				number.append(ab)
				if aa != 0:
					number.append(aa)
					if ab != 0:
						number.append(ab)
		r = "".join(number)
		print r


	mapping = {
		"another [<n>][<direction>]"                : Function(copyLn),
		"undo [<n>]"                                : Function(c_z),
		"delete <direction> <n>"                    : Function(lineDeleter),
		"divide at <symbol> [<margin> spaces]"      : Function(columnMaker),
		"big number <aa><ab><ac><ad>"               : Function(lineNumbers),
		}
	extras = [
		Integer("n", 0, 100, default=0),
		Integer("aa", 0, 9, default=0),
		Integer("ab", 0, 9, default=0),
		Integer("ac", 0, 9, default=0),
		Integer("ad", 0, 9, default=0),
		Integer("margin", 1, 100, default=25),
		Choice("direction",{
			"up"                    :"up",
			"down"                  :"down",
			}, default="down"),

		Choice("symbol",{
			"equals sign"           :"=",
			"colon"                 :":",
			"open paren"            :"(",
			"close paren"           :")",
			}, default="="),
		]


# Create a grammar which contains and loads the command rule.
naminggrammar = Grammar("naming conventions")	# Create a grammar to contain the command rule.
naminggrammar.add_rule(ProgrammingNamingConventions())
naminggrammar.add_rule(cursorManipulator())
naminggrammar.add_rule(DataComparisons())
naminggrammar.add_rule(betterCopy())
naminggrammar.add_rule(pythonCoolShit())
naminggrammar.add_rule(bracketTypes())

naminggrammar.load()
