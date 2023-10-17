import polyglot
from polyglot.text import Text, Word
words = ["preprocessing", "processor", "invaluable", "thankful", "crossed"]
for w in words:
  w = Word(w, language="en")
  print("{:<20}{}".format(w, w.morphemes))