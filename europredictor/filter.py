from .keywords import keywords
import re
    
def filter_by_body(comments):
    one_country = [comment for comment in comments if len(comment.countries) == 1]
    mult_country = [comment for comment in comments if len(comment.countries) > 1]
    return one_country, mult_country

