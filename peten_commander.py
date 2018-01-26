# coding=UTF-8
import os
import subprocess

EXECUTABLE = "python3"
PY_PATH = os.path.join(".","") # Where to find translations.py etc...
PY_SCRIPTS_PATH = os.path.join(".","") # Where to put scripts and where to create temp.py

COMMENTS_BEGIN = "### PETEN TRANSLATION COMMENTS ###"
COMMENTS_END = "### END OF TRANSLATION COMMENTS ###"
DUMMY_COMMENT = "# "+ "המונח_בעברית"+ " = " + "python_or_english_translation"

FRAMERS = {"\"": "\"", "'": "'", "[": "]", "{": "}", "(": ")"}
STRINGERS = ["\"", "'"]
SPACES = [" ","\t", "\r", "\n",",", ":", ";"]
BRACES = ["[", "]", "(", ")", "{", "}"]
OPERATORS = list("+-/*^&%!=<>")
COMMENTS = ["#"]
NEWLINE = os.linesep #"\r\n"

class Commander:
    def __init__(self, app_object=None, debug_mode = False):
        self.debug_mode = debug_mode
        self.app = app_object
        self.dictionary_files = []
        self.translations_file = "/home/lifman/metaxnet/Peten/translations.txt"
        self.reset()
        # For an interactive shell...
        #self.py = subprocess.Popen([EXECUTABLE], stdin=subprocess.PIPE)
        #self.py.stdin.write("# coding=UTF-8"+"\n")
        
    def tokenize(self, text, debug_mode = False):
        i = 0
        in_string = ""
        in_comment = ""
        tokens = []
        token = []
        if debug_mode:
            print(text)
        while i < len(text):
            #If we're inside an open string, add char to current token
            if in_string:
                if text[i] in [chr(8220),chr(8221)]:
                    token.append("\"")
                else:
                    token.append(text[i])
                #Check if char closes the string. If so - we're not in string anymore
                if token[-1] == in_string:
                    in_string = ""
                    tokens.append("".join(token))
                    token = []
                elif text[i] == "\\" and i < len(text)-1:
                    token.append(text[i+1])
                    i = i + 1
                i = i + 1
            elif in_comment:
                token.append(text[i])
                if text[i] == "\n":
                    tokens.append("".join(token))
                    token = []
                    in_comment = ""
                i = i + 1
            elif text[i] in COMMENTS:
                if token:
                    tokens.append("".join(token))                   
                token = [text[i]]
                in_comment = text[i]
                i = i + 1
            elif text[i] in ["\"", "'", chr(8220), chr(8221)]:
                if token:
                    tokens.append("".join(token))
                token = [text[i]]
                if token[0] in [chr(8220),chr(8221)]:
                    token = ["\""]
                in_string = token[0]
                i = i + 1
            elif text[i] in SPACES + BRACES + OPERATORS + ["."]:
                if token:
                    tokens.append("".join(token))
                tokens.append(text[i])
                token = []
                i = i + 1
            else:
                token.append(text[i])
                i = i + 1
                
        if token:
            tokens.append("".join(token))
        if debug_mode:
            print (tokens)
        return tokens

    def _update_translations_with_hebrew_and_code(self, hebrew, code, debug_mode = False):
        if hebrew not in self.translated.keys() and code not in self.translated.values():
            self.translated[hebrew] = code
            return True
        elif hebrew in self.translated.keys() and self.translated[hebrew] == code:
            pass
            return True
        elif hebrew in self.translated.keys() and code in self.translated.values():
            if debug_mode:
                print ("I have a translation for", hebrew, "and", code, "is already taken!")
            return False
        elif hebrew in self.translated.keys() and code not in self.translated.values():
            if debug_mode:
                print ("I have a translation for", hebrew, "-", self.translated[hebrew], ". You suggested", code, ".")
            return False
        elif hebrew not in self.translated.keys():
            existing = [x for x in self.translated if self.translated[x] == code][0]
            if debug_mode:
                print ("Python", code, "was already used to translate", existing, ".")
            return False

    def _update_translations_from_file(self, filename):
        translations = open(filename, "rb").read().decode("utf-8")
        for l in [x.strip() for x in translations.split(NEWLINE)]:
            if " = " in l:
                code, hebrew = l.split(" = ")
                if not self._update_translations_with_hebrew_and_code(hebrew, code):
                    return False
        return True

    def update_translations_from_comments(self, text, debug_mode=False):
        lines = text.split("\n")
        comments_section_flag = False
        for l in [x.strip() for x in lines]:
            if l == COMMENTS_BEGIN:
                comments_section_flag = True
            elif l == COMMENTS_END:
                comments_section_flag = False
            elif comments_section_flag:
                items = l.split(" ")
                if len(items) == 4 and items[0] == "#" and items[2] == "=":
                     if debug_mode:
                         print ("Updating!", items[1], items[3])
                     self._update_translations_with_hebrew_and_code(items[1], items[3])
        
    def add_dictionary_file(self, filename):
        if filename not in self.dictionary_files:
             self.dictionary_files.append(filename)
                
    def reset(self):
        self.translated = {}
        self._update_translations_from_file(self.translations_file)
        self.all_ok = True
        for filename in self.dictionary_files:
            try:
                if not self._update_translations_from_file(filename):
                    self.all_ok = False
                    return 
            except:
                self.all_ok = False
                return
        #
        self.translation_comments = []
        self.entered_commands = []
        
    def handle_command_line(self, text):
        words = self.tokenize(text)
        out = []
        for word in words:
            pyword = self.translate(word)
            out.append(pyword)
        self.entered_commands.append(" ".join(out))
        #
        self.py.stdin.write(" ".join(out)+NEWLINE)
        
    def get_translation_dic(self):
        return self.translated

    def translate(self, word, debug_mode=False):
        if word in self.translated:
            return self.translated[word]
        if word in " +-=%*/.()[]{}:!,<>0123456789":
            return word
        elif word and word[0] in "\"\'" and word[-1] in "\"\'":
            return word
        if debug_mode:
            print ("Got", word, [word], "not in:", end="")
            for k in self.translated.keys():
                print (k, [k], end="")
            print ()
        return word
        
    def _is_illegal(self, word):
        if word[0] in ["#"]:
            return False
        if word[0] in ["\"", "'"] and word[-1] in ["\"", "'"]:
            return False
        for c in word:
            if ord(c) > 127 or ord(c) < 9:
                return True
        return False

    def process(self, filename=None, force_filename=False):
        if not filename or not force_filename:
            filename = PY_SCRIPTS_PATH+"temp.py"
        if "# coding=UTF-8" in self.entered_commands:
            self.entered_commands.remove("# coding=UTF-8")
        self.entered_commands = ["# coding=UTF-8"]+self.entered_commands+self.translation_comments
        print(type(self.entered_commands))
        #f = open(PY_SCRIPTS_PATH+"temp.py", "wb")
        f = open(filename, "wb")
        new_text = NEWLINE.join(self.entered_commands)
        print (new_text)
        f.write(bytes(new_text,"utf8"))
        f.close()
        return new_text

    def run(self, filename=None):
        print("Run")
        if not filename:
            filename = PY_SCRIPTS_PATH+"temp.py"
        subprocess.call([EXECUTABLE, filename])
        print("Done")


def process_and_run_no_GUI(filename, debug_mode=False, run_mode=True):
    commander = Commander(None, debug_mode)        
    text = open(filename, "r").read()
    try:
        if "### PETEN TRANSLATION COMMENTS ###" in text:
            translations_text = text[text.index("### PETEN TRANSLATION COMMENTS ###"):]
            print("TRANSLATIONS:", translations_text)
        else:
            translations_text = open(filename+".translations", "rb").read().decode("utf8")
        commander.update_translations_from_comments(translations_text)
        translation_comments = translations_text.split(NEWLINE)
    except:
        text = text.decode("utf8")
        text = "".join([COMMENTS_BEGIN] + [DUMMY_COMMENT] + [COMMENTS_END])
        f = open(filename+".translations", "wb")#
    
        f.write(bytes(text,"utf8"))
        f.close()
        translation_comments = []

    needing_translation = []
    lines = str(text).split(NEWLINE)
    for l in lines:
        #print (l, type(l))
        words = commander.tokenize(l) #.decode("utf-8"))
        #print ("WORDS:"+NEWLINE, words)
        pyline = []
        for word in words:
            pyword = commander.translate(word)
            if pyword == word and commander._is_illegal(word):
                if word not in needing_translation:
                    needing_translation.append(word)
                    pyword = "_word"+str(len(needing_translation))
                    translation_comments.append("# %s = %s" % (word, pyword))
                else:
                    pyword = "_word"+str(needing_translation.index(word) + 1)
            pyline.append(pyword)
        commander.entered_commands.append("".join(pyline))
    if COMMENTS_BEGIN not in translation_comments:
        commander.translation_comments = [COMMENTS_BEGIN] + translation_comments[:] + [COMMENTS_END]
    if debug_mode:
        print (NEWLINE.join(commander.entered_commands))
        print (NEWLINE.join(translation_comments))
    outfile = None
    print ("Filename:", filename)
    if filename.endswith(".peten"):
        outfile = filename.replace(".peten", ".py")
    print ("Outfile=", outfile)
    if run_mode:
        commander.process(outfile, force_filename=True)
        commander.run(outfile)
    else:
        commander.process(outfile, force_filename=True)
        return outfile
