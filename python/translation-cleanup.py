#!/usr/bin/env python
import os
import re
import fnmatch
import toml
import collections
from googletrans import Translator

## set this
lang = "es"
gtranslate = False
translator = Translator()
# fix this program to work in batch mode possibly
# https://pypi.org/project/googletrans/

def add_comments(filename):
    exists = os.path.isfile(filename)
    print("\n")
    if not exists:
        print("file" + filename + " not found")
    else: 
        print("file" + filename + " found")
    f = open(filename, 'r', encoding='utf-8')
    content_new = re.sub(r'file \=', '# file =', f.read(), flags = re.M)
    content_new = re.sub(r'english \=', '# english =', content_new, flags = re.M)
    content_new = re.sub(r'gtrans \=', '# gtrans =', content_new, flags = re.M)
    
    # print (content_new)
    f.close()
    f = open(filename, 'w', encoding='utf-8')
    f.write(content_new)
    f.close()

def commentsToTomlFields(filename):
    exists = os.path.isfile(filename)
    print("\n")
    if not exists:
        print("file" + filename + " not found")
    else: 
        print("file" + filename + " found adding back file location field")
    f = open(filename, 'r', encoding='utf-8')
    content_new = re.sub('# file =', 'file =', f.read(), flags = re.M)
    content_new = re.sub('# english =', 'english =', content_new, flags = re.M)
    content_new = re.sub('# gtrans =', 'gtrans =', content_new, flags = re.M)

    # print (content_new)
    f.close()
    f = open(filename, 'w', encoding='utf-8')
    f.write(content_new)
    f.close()   

translations = {}
## starting in the layouts directory matching files ending in .html
wdir = "layouts"
filePattern = "*.html"
## get files recursively 
for path, dirs, files in os.walk(os.path.abspath(wdir)):
    for filename in fnmatch.filter(files, filePattern):
        filepath = os.path.join(path, filename)
        print("working on file " + filename)
        f = open(filepath, 'r',encoding='utf-8')
        # Feed the file text into findall(); it returns a list of all the found strings
        strings = re.findall(r'{{\s*T\s+"(.+?)"\s*}}', f.read())
        sortedstrings = sorted(list(set(strings)))
        for string in sortedstrings:
            ## check to see if it has already been found and if so add another file reference 
            if string in translations:
                translations[string]["file"] = translations[string]["file"] + " , " + filename
            else:
                translations[string] = {}
                translations[string]["file"] = filename
                translations[string]["other"] =  string.replace("_"," ")
                if gtranslate:
                    tobject = translator.translate(translations[string]["other"] , dest=lang)
                    translations[string]["other"] = tobject.text 


sorted_translations = collections.OrderedDict(sorted(translations.items(), key=lambda t: t[0]))

tomlfname = os.path.join("i18n", lang + ".toml")
commentsToTomlFields(tomlfname)
parsed_toml = toml.load(tomlfname)
sortedToml = collections.OrderedDict(sorted(parsed_toml.items(), key=lambda t: t[0]))

# # print (strings)
for match in sorted_translations.keys():
    if match in sortedToml.keys():
        # print ( match + " found in tomlfile")
        # just need to update or create the file location information then
        sortedToml[match]["file"] = sorted_translations[match]["file"]
    else:
        # print ( match + " not found in tomlfile")
        sortedToml[match] = sorted_translations[match]
sortedToml = collections.OrderedDict(sorted(sortedToml.items(), key=lambda t: t[0]))


##array of englist text to be translated
englishItems=[]

for item in sortedToml:
    if "english" not in sortedToml[item]:
       sortedToml[item]["english"] = item.replace("_"," ")
       englishItems.append(item.replace("_"," "))
englishItems = sorted(list(set(englishItems)))

translations = translator.translate(englishItems, dest='es')
#translations = translator.translate(["Price","Pricing"], dest='es')

for translation in translations:
   print(translation.origin, ' -> ', translation.text)

for item in sortedToml:
    if "gtrans" not in sortedToml[item]:
        ## assuming the english translation is there
        ## as it should be
        ## loop through translations object to find a match
        for translation in translations:
            if translation.origin == sortedToml[item]["english"]:
                sortedToml[item]["gtrans"] = translation.text
                ## if english in not the default langauge and English matches other default translation
                # then put in google translate
                if sortedToml[item]["other"] == sortedToml[item]["english"]:
                    if lang != "en":
                        sortedToml[item]["other"] =  translation.text

# tomlfname = "test.txt"

outfile = open(tomlfname, 'w',encoding='utf-8')
toml.dump(sortedToml, outfile)
outfile.close()
add_comments(tomlfname)