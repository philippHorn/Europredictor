import spacy

print("working...")
en_nlp = spacy.load('en')
print("loaded")
en_doc = en_nlp(u'Hello, world. Here are two sentences.')
print(en_doc)