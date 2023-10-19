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

for package in packages_to_check:
    check_ins(package)

def dl_lang(g):
    if g == "zh":
        result = subprocess.run(['polyglot', 'download', 'morph2.zh'], stdout=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("Polyglot Chinese package has been installed.")
        else:
            print("Failed to install Polyglot Chinese package")
import polyglot
import random
from polyglot.downloader import downloader
from polyglot.text import Text, Word
dir_nm =  '/content/drive/MyDrive/MLUCH/'
dl_lang("zh")
five = []
oh_five = []
oh_seven = []
for dir_name, subdirs, filenames in os.walk(dir_nm):
    for filename in filenames:
        if filename.endswith('.cha'):
            cha_file_path = os.path.join(dir_name, filename)
            utterance_count = 0
            morpheme_count = 0
            total_mlu = 0
# here's the difference from 100.py, it will calculate each file's MLU 1000 times
            for i in range(1000):
                with open(cha_file_path, 'r', encoding='utf-8') as cha_file:
                    lines = list(cha_file)

# here's the difference from 100.py, here it randomly shuffle the lines to randomize the order
                    random.shuffle(lines)

                    for line in lines:
                        if line.startswith('*CHI'):
                            line = re.sub(r'[A-Za-z0-9!@#$%^&*()_+{}\[\]:;"\'<>,.?/\\|~`= ‡]', '', line)
                            w = Text(line)
                            w.language = "zh"
                            if len(w.words) == 0:
                                continue
                            morpheme_count += len(w.words)
                            utterance_count += 1
                            if utterance_count >= 100:
                                break

                    mlu = morpheme_count / utterance_count if utterance_count > 0 else 0

#stores the output in a new variable called total_mlu
                    total_mlu += mlu  


# Calculate the average MLU for the 1000 iterations
            average_mlu = total_mlu / 1000
            print(f'{filename} Average MLU for 100 utterances over 1000 iterations: {average_mlu:.2f}')

                 