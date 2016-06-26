import re
from copy import deepcopy
from pattern.en import parse, parsetree
from nltk.tokenize import sent_tokenize
from .keywords import keywords


def split_to_country(comment):
    """
    Takes a comment object and analyses the body attribute. 
    Returns the following:
    - No country detected in comment.body            ---> Empty list
    - One country detected in comment.body           ---> List containing unaltered comment
    - More than one country detected in comment.body ---> A list of comments for each country detected where comment.body
                                                          is the smallest clause found containing said country.
    
    :param comment: comment object
    :return: list of comment objects
    """
    
    # Split the cody string into component sentences
    blurb = comment.body
    sentences = sent_tokenize(blurb)

    # Filter sentences into one and multi country. Remove sentences with no country references.
    sents_with_one_country, sents_with_multi_country = _filter_on_country_count(sentences)
    
    # Break down sentences with multiple country references into clauses.
    clauses = [_sub_clause(sentence) for sentence in sents_with_multi_country]
    clauses = [item for sublist in clauses for item in sublist] #F Flatten the nested lists
    
    # Filter clauses into one and multi county. Remove clauses with no country references.
    clauses_with_one_country, clauses_with_multi_country = _filter_on_country_count(clauses)
    
    # We don't break down clauses with multiple countries any further.
    strings_with_country = sents_with_one_country + clauses_with_one_country + clauses_with_multi_country

    # Build new comment objects
    comment_list = []
    for string in strings_with_country:
        new_comment = deepcopy(comment)
        new_comment.body = string
        new_comment.find_countries()
        comment_list.append(new_comment)

    return comment_list


def _sub_clause(string):
    """
    Takes a string (which should be a single sentence) and returns a list of strings of clauses of the sentence.
    
    :param string: string
    :return: list of strings
    """
    
    # Spit into sentences and tag the words with parts of speech
    tagged = parsetree(string, relations=True)
    
    # Check that we only have one sentence.
    if len(tagged) != 1:
        raise ValueError()

    # Find the words (conjunctions "CC" and commas ",") which will separate our clauses ensuring we don't use
    # conjuctions or commas that belong to a word chunk.
    sentence = tagged[0]
    separators = [word for word in sentence if (word.type in ["CC", ","] and word.chunk == None)]

    # Slice our original sentence based on the separators and return as a list of strings.
    clauses = _slice_sentence(sentence, separators)
    return [" ".join([word.string for word in word_list]) for word_list in clauses]


def _slice_sentence(sentence, seperators):
    """
    Slices a sentence object and a list of word objects (separators) within that sentence. Slices the sentence returning
    a list of clauses (also sentence objects) based on the positions of the separators.
    
    :param sentence: sentence object
    :param seperators: list of word objects
    :return: list of sentence objects
    """
    
    start = 0
    sentences = []
    for word in seperators:
        sentences.append(sentence[start:word.index])
        start = word.index + 1 # +1 so not to include the seperator itself in the clause
    sentences.append(sentence[start:])
    return sentences


def _count_countries(string):
    """
    Count the number of unique countries mentioned in the string.
    
    :param string: string
    :return: int
    """
    
    return len([country for country, patterns in keywords.items()
                if any((re.search(pattern, string, flags=re.IGNORECASE)
                        for pattern in patterns))])


def _filter_on_country_count(string_list):
    """
    # Takes a list of srings and returns two lists of strings, one where the strings contain a reference to exactly one
    etcountry, and one where the srtings contain references to multiple countries.
    
    :param string_list: list of strings
    :return: 2 lists of stings
    """
    
    country_numbers = [_count_countries(string) for string in string_list]
    one_country = [string for string, number in zip(string_list, country_numbers) if number == 1]
    mult_country = [string for string, number in zip(string_list, country_numbers) if number > 1]
    return one_country, mult_country