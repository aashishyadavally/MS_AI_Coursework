import nltk
from nltk import *
from homework6_1 import  display
from homework6_2a import update_init_chart as init_chart
from homework6_2a import update_complete_chart as complete_chart


def treesOfChart(chart, category, span):
    """Prints tree from chart parser table

    Arguments
    ---------
        chart (list):
            List of lists which represents the chart parser table
        category (str):
            Represents category on tree
        span (tuple):
            Represents span of chart entry
    """
    i, j = span[0], span[1]
    if chart[i][j]:
        for entry in chart[i][j]:
            # entry[1] refers to the rule.
            # By splitting on "->", we get right hand side, which
            # is a tuple. If length of that string is greater than 1,
            # then it is a terminal
            print(entry[0], entry[1], entry[2])
            left = entry[1].split('->')[1].strip().split(',')[0].strip().split('(')[1]
            right = entry[1].split('->')[1].strip().split(',')[1].strip().split(')')[0]

            if len(right) == 0 and str(entry[0]) == category:
                return [nltk.tree.Tree(category, [entry[1]])]
            else:
                s1 = treesOfChart(chart, left, (i, entry[2]))
                s2 = treesOfChart(chart, right, (entry[2], j))
                if s1 and s2:
                    return [nltk.tree.Tree(category, [t1,t2]) for t1 in s1 for t2 in s2]


# MAIN FUNCTION
# L1 Grammar taken from Pg. 227, Ch. 11.2, Jufarsky Ed.3
L1_Grammar = nltk.CFG.fromstring("""
    S -> X1 VP
    S -> NP VP
    X1 -> Aux NP
    S -> 'book' | 'include' | 'prefer'
    S -> Verb NP
    S -> X2 PP
    S -> Verb PP
    S -> VP PP
    NP -> 'I' | 'she' | 'me'
    NP -> 'TWA' | 'Houston'
    NP -> Det Nominal
    Nominal -> 'book' | 'flight' | 'meal' | 'money'
    Nominal -> Nominal Noun
    Nominal -> Nominal PP
    VP -> 'book' | 'include' | 'prefer'
    VP -> Verb NP
    VP -> X2 PP
    X2 -> Verb NP
    VP -> Verb PP
    VP -> VP PP
    PP -> Preposition NP
    Det -> 'that' | 'this' |'the' |'a'
    Noun -> 'book' | 'flight' |'meal' |'money'
    Verb -> 'book' | 'include' |'prefer'
    Prononun -> 'I' |'she' | 'me'
    Aux -> 'does'
    Preposition -> 'from' | 'to' | 'on' | 'near' | 'through'
""")

tokens = "on the flight through Houston".split()
initial_chart = init_chart(tokens, L1_Grammar)
print('Displaying Initial Set Chart Parser Table for L1 Grammar...')
display(initial_chart, tokens)

final_chart = complete_chart(initial_chart, tokens, L1_Grammar)
print('Displaying Complete Set Chart Parser Table for L1 Grammar...')
display(final_chart, tokens)

span = (0, (len(tokens)))
a = treesOfChart(final_chart, 'S', span)
print(a[0])
