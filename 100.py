# I import the stuff I need, don't worry about this
import pkgutil
import subprocess
import os
import re

#I check if the system has the packages this script needs, if not, it installs them
#this part will be error-free on Linux and Google Colab, very much not so on Windows
packages_to_check = ["polyglot", "pycld2", "pyicu", "morfessor", "six"]

def check_ins(package_name):
    if pkgutil.find_loader(package_name) is None:
        print(f"{package_name} is not installed. Installing...")
        result = subprocess.run(['pip', 'install', package_name], stdout=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"{package_name} has been installed.")
        else:
            print(f"Failed to install {package_name}.")
    else:
        print(f"{package_name} is already installed.")

for package in packages_to_check:
    check_ins(package)


#Now I import Polyglot and its needed components
import polyglot
from polyglot.downloader import downloader
from polyglot.text import Text, Word

#this part downloads the language data, in this case zh, aka Chinese
def dl_lang(g):
    if g == "zh":
        result = subprocess.run(['polyglot', 'download', 'morph2.zh'], stdout=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("Polyglot Chinese package has been installed.")
        else:
            print("Failed to install Polyglot Chinese package")

dl_lang("zh")

#this is where I specify the folder in which to look for .cha files
dir_nm =  '/content/drive/MyDrive/MLUCH/'

#Now I start to look for all files in that directory, stores all filenames in variable "filenames"
for dir_name, subdirs, filenames in os.walk(dir_nm):
    for filename in filenames:
        count = 0
#if filename ends with .cha, lol this is pretty straightforward
        if filename.endswith('.cha'):
            cha_file_path = os.path.join(dir_name, filename)

# I initialize the variables for counting utterances and morphemes, it's 0 rn
            utterance_count = 0
            morpheme_count = 0

# I open the CHA file
            with open(cha_file_path, 'r', encoding='utf-8') as cha_file:

#I store every line in the cha file in the variable "lines"
                lines = list(cha_file)

#I now look through every line
                for line in lines:

#and if that line starts with "*CHI" (essentially ignoring all lines that doesn't start with *CHI)
                    if line.startswith('*CHI'):

# I remove all unnecessary characters, which are those: [A-Z a-z 0-9 !@#$%^&*()_+{}\[\]:;"\'<>,.?/\\|~`= ‡]
                        line = re.sub(r'[A-Za-z0-9!@#$%^&*()_+{}\[\]:;"\'<>,.?/\\|~`= ‡]', '', line)

#Now we start using the nifty "Text()" tool from polyglot to turn each sentence into a set of words, which is basically morphemes in Chinese
#as defined by the document Jessica sent in group
                        w = Text(line)
                        w.language = "zh"

#if that sentence is just empty after I remove all unnecessary characters and turned them into individual words, the script will ignore it
                        if len(w.words) == 0:
                          continue

#these 2 lines are for outputting each utterance, not important
                        count += 1
                        print(f"Line {count}: {w.words}")

#Morphemes are counted here, determined by the length of the set, aka how many words are there in the set?
                        morpheme_count += len(w.words)

#Each sentence counts as an utterance
                        utterance_count += 1

#from here it loops back and processes another sentence, but we only count 100 utterances, so if 100 utterances are counted,
#this loop stops
                        if utterance_count >= 100:
                          break

#MLU is calculated here...if the utterance count is more than 0     
            mlu = morpheme_count / utterance_count if utterance_count > 0 else 0

#This outputs "005_3.cha MLU for 100 utterances: 2.34" so i can copy the output
# .2f means just the 2 decimal points
            print(f'{filename} MLU for 100 utterances: {mlu:.2f}')