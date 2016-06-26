from pattern.en import parse, parsetree
from pattern.en import pprint
from europredictor.subclause import _sub_clause

print(_sub_clause("Ireland is good but France is better"))
# print(_sub_clause("Ireland and France are good"))
# print(_sub_clause("Ireland is better than France"))
print(_sub_clause("Russia were really good but France were terrible"))
print(_sub_clause("Wales and England were really good but France were terrible and Turkey didn't show up."))


# def chinked_words():
#     try:
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             tagged = nltk.pos_tag(words)

#             # a chunk is a regexp to match defined in the way shown below
#             chunkGram = r"""Chunk: {<.*>+}
#                                     }<CC>{"""
#             # the above works as follows:
#             #   "Chunk:" can be whatever we want (you caould have "Foobar: instead
#             #   "{}" denotes a chunk to be matched
#             #   "<>" encloses the regexp
#             #   "." is a regexp for ANY character other than newline
#             #   "*" means it's matched from 0 to infinite times
#             #       so <.*> is a regexp to match any character 0 to infinite times
#             #   "+" means matched ATLEAST once
#             #       so {<.*>+} means match a piece of text (in the tags!) with any character from 0 to infinite occurances, atleast once
#             #   "}{" denotes a chink to be matched
#             #   "<>" encloses the regexp
#             #   "CC" is a regexp for matching CC exactly. The conjunction tag is CC so this is what we wish to match
#             #       so <CC> is a regexp to match any CC
#             #       so }<CC>{ means match a the tag CC exactly (the conjuntion tag - this will not be included in the returned text

#             chunkParser = nltk.RegexpParser(chunkGram)
#             chunked = chunkParser.parse(tagged)
#             print(chunked)

#     except Exception as e:
#         print(str(e))

# chinked_words()