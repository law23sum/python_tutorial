import spacy
from spacytext import main

nlp = spacy.load('en')
f = open("test.txt", "rb")
contents = f.read()
doc = nlp(contents[:100000].decode('utf8'))
main(doc)
