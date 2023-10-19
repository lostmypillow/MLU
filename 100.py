import pkgutil
import subprocess
import os
import re

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
def dl_lang(g):
    if g == "zh":
        result = subprocess.run(['polyglot', 'download', 'morph2.zh'], stdout=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("Polyglot Chinese package has been installed.")
        else:
            print("Failed to install Polyglot Chinese package")


for package in packages_to_check:
    check_ins(package)

import polyglot
from polyglot.downloader import downloader
from polyglot.text import Text, Word

dir_nm =  '/content/drive/MyDrive/MLUCH/'
#input("Directory Path (if on Win add additional (\): ")
#lang_nm = input("language? en or zh?")
dl_lang("zh")


for dir_name, subdirs, filenames in os.walk(dir_nm):
    for filename in filenames:
        if filename.endswith('.cha'):
            cha_file_path = os.path.join(dir_name, filename)

            # Initialize variables for counting utterances and morphemes
            utterance_count = 0
            morpheme_count = 0

            # Open the CHA file, convert to text, and calculate MLU
            with open(cha_file_path, 'r', encoding='utf-8') as cha_file:
                lines = list(cha_file)

                # Randomly shuffle the lines to randomize the order
               # random.shuffle(lines)

                for line in lines:
                    if line.startswith('*CHI'):


                        line = re.sub(r'[A-Za-z0-9!@#$%^&*()_+{}\[\]:;"\'<>,.?/\\|~`= ‡]', '', line)
                      
                        #print(line)
                        w = Text(line)
                        w.language = "zh"
                      #  print (w.words)
                        if len(w.words) == 0:
                          continue

                        morpheme_count += len(w.words)
                      #  print("current count:", morpheme_count)
                        utterance_count += 1
                        #print(f"Line {utterance_count}: ", w.words)
                        if utterance_count >= 100:
                          break
              
            mlu = morpheme_count / utterance_count if utterance_count > 0 else 0

            # Print the MLU for each file
            print(f'{filename} MLU for 100 utterances: {mlu:.2f}')