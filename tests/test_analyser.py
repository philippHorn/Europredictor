import europredictor.analyser as analyser


#Difference between comment and clause:
# clause has only one country
# clause body is only one clause long
# clause has team assigned to it
class test_clause(object):
    def __init__(self):
        test_clause.body = "Hello I'm a positive test clause"
        test_clause.url = "www.test.com"
        test_clause.username = "Bob"
        test_clause.flair = "Some flair text"
        test_clause.thread_title = "Football is the shit"
        test_clause.thread_url = "www.somewebaddress.com"
        test_clause.posted = 1466640253
        test_clause.country = 'France'


tc = test_clause()

atc = analyser.analyse(tc)
print(atc.polarity_scores)

analyser.store_analysed_clause(atc, overwrite = False)




c = analyser._connect_db('europredictor.db')
cursor = c.cursor()

for row in cursor.execute("SELECT * FROM clauses"):
    print row