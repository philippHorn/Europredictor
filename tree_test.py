import europredictor.stat_parser as par
import nltk

parser = par.Parser()

sentences = ["Ireland is good but Turkey is better", "France is nice but so is Italy", "Wales did better than turkey", "The Swiss played better than the Italian"]
sentences += ["I like Ireland and Turkey", "Spain and France are great", "Wales is good, England is also good"]

def search_by_string(tree, string):
    print tree, tree[0]
    if type(tree[0]) == str:
        return tree
    right_subtree = [subtree for subtree in tree if string.lower() in 
                    (tree_str.lower() for tree_str in subtree.leaves())]
    return search_by_string(right_subtree[0], string) if right_subtree else None

def search_by_label(tree, label):
    if tree.label() == label:
        return tree
    subtrees = [subtree for subtree in tree if not type(subtree) == str]
    for subtree in subtrees:
        result = search_by_label(subtree, label)
        if result: return result

for sentence in sentences:
    tree = parser.parse(sentence)
    tree = nltk.ParentedTree.convert(tree)
    tree.pretty_print()
    #tree.pprint()

print tree.leaves()
print search_by_label(tree, ",").left_sibling()