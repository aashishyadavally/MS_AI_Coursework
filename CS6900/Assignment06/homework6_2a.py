import nltk
from nltk import Nonterminal, Production
from homework6_1 import tokens as groucho_tokens
from homework6_1 import groucho_grammar2 as groucho_grammar
from homework6_1 import display


def update_init_chart(tokens, grammar):
    """Updates diagonal elements of chart

    Arguments:
    ----------
        tokens (list):
            List of words in input sentence
        grammar (list):
            List of production rules in the grammar
    """
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    num_tokens = len(tokens)
    # Defining empty chart
    init_chart = [[None for i in range(num_tokens+1)] for j in range(num_tokens+1)]
    for i in range(num_tokens):
        productions = grammar.productions(rhs=tokens[i])
        precedent = [production.lhs() for production in productions]
        antecedent = [production.rhs() for production in productions]
        rules = [f'{precedent[i]} -> {antecedent[i]}' for i in range(len(productions))]
        init_chart[i][i+1] = [(precedent[i], rules[i], 0) for i in range(len(productions))]
    return init_chart


def update_complete_chart(chart, tokens, grammar, trace=False):
    """Updates non-diagonal elements of chart

    Arguments:
    ----------
        chart (list):
            List of list containing chart algorithm elements
        tokens (list):
            List of words in input sentence
        grammar (list):
            List of production rules in the grammar
    """
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    num_tokens = len(tokens)
    for span in range(2, num_tokens + 1):
        for start in range(num_tokens + 1 - span):
            end = start + span
            temp_categories, temp_rules = [], []
            for mid in range(start + 1, end):
                nt1s, nt2s = chart[start][mid], chart[mid][end]
                if len(nt1s) != 0 and len(nt2s) != 0:
                    for nt1 in nt1s[0]:
                        for nt2 in nt2s[0]:
                            if nt1 and nt2 and (nt1, nt2) in index:
                                p = Production(index[(nt1, nt2)], (Nonterminal(nt1), Nonterminal(nt2)))                          
                                temp_rules.append(f'{p._lhs} -> {p._rhs}')
                                temp_categories.append(index[(nt1, nt2)])
            chart[start][end] = [(temp_categories[i], temp_rules[i], mid) for i in range(len(temp_rules))]
    return chart



# Main Function
groucho_init_chart = update_init_chart(groucho_tokens, groucho_grammar)
print('Displaying Initial Set Chart Parser Table for Groucho Grammar...')
display(groucho_init_chart, groucho_tokens)

updated_chart = update_complete_chart(groucho_init_chart, groucho_tokens, groucho_grammar)
print('Displaying Complete Set Chart Parser Table for Groucho Grammar...')
display(updated_chart, groucho_tokens)

span = (0, len(groucho_tokens))

