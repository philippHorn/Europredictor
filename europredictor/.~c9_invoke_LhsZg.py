import re
from copy import deepcopy
from pattern.en import parse, parsetree
from nltk.tokenize import sent_tokenize 
from .keywords import keywords

def split_to_country(comment):
    string = comment.body
    sentences = _split_sentences(string)
    
    
    #filter sentences that have no country
    sents_with_one_country, sents_with_multi_country =  _filter_on_country_number(sentences)
    clauses =  [_sub_clause(sentence) for sentence in sents_with_multi_country]
    clauses = [item for sublist in clauses for item in sublist]
    clauses_with_one_country, clauses_with_multi_country = _filter_on_country_number(clauses)
    
    
    all_strings = sents_with_one_country + clauses_with_one_country + clauses_with_multi_country
    
    comment_list = []
    #build comment objects
    for string in all_strings:
        new_comment = deepcopy(comment)
        new_comment.body = string
        new_comment.find_countries()
        comment_list.append(new_comment)

    
    return comment_list


def _sub_clause(string):
    # check if multiple subject (not in same group), if so check if they are multiple countries
    # if so, split on CC or ,
    
    text = parsetree(string, relations=True)
    
    if len(text) != 1:
        raise ValueError()
        
    sentence = text[0]
    seperators = [word for word in sentence if (word.type in ["CC", ","] and word.chunk == None)]

        if i ==
    return [" ".join([word.string for word in word_list]) for word_list in sentences]


def slice_sentence(sentence, seperators):
    start = 0
    sentences = []
    for word in seperators:
        sentences.append(sentence[start:word.index])
        start = word.index + 1 
    sentences.append(sentence[start:])
    return sentences

def _split_sentences(string):
    return sent_tokenize(string)

def _count_countries(string):
    """find all countries mentioned in the comment"""
    return len([country for country, patterns in keywords.items() 
                if any((re.search(pattern, string, flags=re.IGNORECASE)
                for pattern in patterns))])

def _filter_on_country_number(string_list):
    # return list with one country, and list with multiple country
    country_numbers = [_count_countries(string) for string in string_list]
    one_country =  [string for string, number in zip(string_list, country_numbers) if number == 1]
    mult_country =  [string for string, number in zip(string_list, country_numbers) if number > 1]
    return one_country, mult_country