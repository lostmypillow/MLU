import os
import re
k  = input("hello?")
# Define the root directory where the files are located
root_directory = 'C:\\Users\\User\\Downloads\\lk\\d'  # Replace with the actual path

# Iterate through the directories and files
for dir_name, subdirs, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename.endswith('.cha'):
            cha_file_path = os.path.join(dir_name, filename)

            # Define the output text file path in the same directory
            text_file_path = os.path.join(dir_name, 'text_files', f'{os.path.splitext(filename)[0]}.txt')

            # Ensure the 'text_files' directory exists
            os.makedirs(os.path.dirname(text_file_path), exist_ok=True)

            # Initialize variables for counting utterances and morphemes
            utterance_count = 0
            morpheme_count = 0

            # Open the CHA file, convert to text, and calculate MLU
            with open(cha_file_path, 'r', encoding='utf-8') as cha_file:
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    for line in cha_file:
                        if line.startswith('*CHI'):
                            # Remove text within brackets and the brackets themselves
                            line = re.sub(r'\[[^\]]*\]', '', line)
                            # Remove all non-Chinese characters and symbols
                            line = re.sub(r'[^\u4e00-\u9fff\s]', '', line)
                            # Split the line into words (morphemes)
                            words = line.split()
                            # Increment the morpheme count by the number of words in the line
                            morpheme_count += len(words)
                            # Increment the utterance count
                            utterance_count += 1
                            # Write the filtered line to the text file
                            text_file.write(line)

            # Calculate MLU for the file
            mlu = morpheme_count / utterance_count

            # Print the MLU for each file
            print(f'{filename} MLU: {mlu:.2f}')
