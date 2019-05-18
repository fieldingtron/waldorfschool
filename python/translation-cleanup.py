#!/usr/bin/env python
import os
import re
import fnmatch
import toml
import collections
from googletrans import Translator

# set the language 
# set whether to use google translate or not

lang = "es"
translator = Translator()

# this function does regex match to convert three toml fields into comment fields
def add_comments(filename):
    exists = os.path.isfile(filename)
    if not exists:
        print("\nfile" + filename + " not found")
    f = open(filename, 'r', encoding='utf-8')
    content_new = re.sub(r'file \=', '# file =', f.read(), flags = re.M)
    content_new = re.sub(r'english \=', '# english =', content_new, flags = re.M)
    content_new = re.sub(r'gtrans \=', '# gtrans =', content_new, flags = re.M)
    f.close()
    f = open(filename, 'w', encoding='utf-8')
    f.write(content_new)
    f.close()

# this function does regex match to convert three toml comments into toml fields
def commentsToTomlFields(filename):
    exists = os.path.isfile(filename)
    if not exists:
        print("\nfile" + filename + " not found")
    f = open(filename, 'r', encoding='utf-8')
    content_new = re.sub('# file =', 'file =', f.read(), flags = re.M)
    content_new = re.sub('# english =', 'english =', content_new, flags = re.M)
    content_new = re.sub('# gtrans =', 'gtrans =', content_new, flags = re.M)
    f.close()
    f = open(filename, 'w', encoding='utf-8')
    f.write(content_new)
    f.close()   

tmp_translations = {}

# first build a list of translation strings found in the HTML files
# starting in the layouts directory matching files ending in .html
# and going through recursively
wdir = "layouts"
filePattern = "*.html"

for path, dirs, files in os.walk(os.path.abspath(wdir)):
    for filename in fnmatch.filter(files, filePattern):
        filepath = os.path.join(path, filename)
        print("working on file " + filename)
        f = open(filepath, 'r',encoding='utf-8')
        # Feed the file text into findall(); it returns a list of all the found strings
        # regex pattern to match {{T "translation text"}}
        strings = re.findall(r'{{\s*T\s+"(.+?)"\s*}}', f.read())
        # returning a list of unique sorted strings    
        sortedstrings = sorted(list(set(strings)))
        for string in sortedstrings:
            ## check to see if it has already been found and if so add another file reference 
            if string in tmp_translations:
                tmp_translations[string]["file"] = tmp_translations[string]["file"] + " , " + filename
            else:
                tmp_translations[string] = {}
                tmp_translations[string]["file"] = filename
                tmp_translations[string]["other"] =  string.replace("_"," ")

# creating an ordered dictionary of strings
sorted_translations = collections.OrderedDict(sorted(tmp_translations.items(), key=lambda t: t[0]))

# test for and then create toml file if it doesnt exist
tomlfname = os.path.join("i18n", lang + ".toml")
exists = os.path.isfile(tomlfname)
print("\n")
if not exists:
    print("creating tomlfile:" + tomlfname + " not found making ")
    from pathlib import Path
    Path(tomlfname).touch()
else: 
    print("working on tomlfile:" + tomlfname  )

# remove the comment fields to make them tomlfile
commentsToTomlFields(tomlfname)
tomldata = toml.load(tomlfname)
#sortedToml = collections.OrderedDict(sorted(parsed_toml.items(), key=lambda t: t[0]))

# go through the translation strings and see if there is a match 
for match in sorted_translations.keys():
    # if a matching toml data entry is found 
    if match in tomldata.keys():
        # print ( match + " found in tomlfile")
        # just need to update or create the file location information then
        tomldata[match]["file"] = sorted_translations[match]["file"]
    else:
        # print ( match + " not found in tomlfile")
        tomldata[match] = sorted_translations[match]
sortedToml = collections.OrderedDict(sorted(tomldata.items(), key=lambda t: t[0]))


# could do this one at a time but perhaps more effective to translate in batch mode
# make array of english text to be translated
englishItems=[]

# check if we have done this before on a previous pass
# if not then added english field to match gtrans field in next loop
# fill in the english field for later use and comparison
for item in sortedToml:
    if "english" not in sortedToml[item]:
       sortedToml[item]["english"] = item.replace("_"," ")
       englishItems.append(item.replace("_"," "))
englishItems = sorted(list(set(englishItems)))

# if it is not english we are translating into
# translation variables
translations = []
if lang != "en":
    translations = translator.translate(englishItems, dest=lang)
    for translation in translations:
        print(translation.origin, ' -> ', translation.text)

# sortedToml has the file location and english translation
# and possibly google tranlation   
# here we go through the sortedToml file 
# adding gtrans field if not found 
# gtrans aka automated google translation
for item in sortedToml:
    if "gtrans" not in sortedToml[item]:
        # we have english translation field to we look for a match
        for translation in translations:
            # if a matching english translation is found
            if translation.origin == sortedToml[item]["english"]:
                # then fill the corresponding google translation
                sortedToml[item]["gtrans"] = translation.text
                # now that we have the google tranlation field
                # check to see if the language is not english and
                # if the default translation matches the english
                # then correct to a language appropriate guess
                if lang != "en" and sortedToml[item]["other"] == sortedToml[item]["english"]:
                    sortedToml[item]["other"] =  translation.text

# tomlfname = "test.txt"

outfile = open(tomlfname, 'w',encoding='utf-8')
toml.dump(sortedToml, outfile)
outfile.close()
add_comments(tomlfname)
