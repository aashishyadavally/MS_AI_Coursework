import nltk


def init_wfst(tokens, grammar):
    """Updates diagonal elements of chart

    Arguments:
    ---------
        tokens (list):
            List of words in input sentence
        grammar (list):
            List of production rules in the grammar     
    """
    num_tokens = len(tokens)
    wfst = [[None for i in range(num_tokens+1)] for j in range(num_tokens+1)]
    for i in range(num_tokens):
        productions = grammar.productions(rhs=tokens[i])
        wfst[i][i+1] = [production.lhs() for production in productions]
    return wfst


def complete_wfst(wfst, tokens, grammar, trace=False):
    """Updates non-diagonal elements of chart

    Arguments:
    ---------
        wfst
        tokens (list):
            List of words in input sentence
        grammar (list):
            List of production rules in the grammar     
    """
    index = dict((p.rhs(), p.lhs()) for p in grammar.productions())
    num_tokens = len(tokens)
    for span in range(2, num_tokens+1):
        for start in range(num_tokens+1-span):
            end = start + span
            temp = []
            for mid in range(start+1, end):
                nt1s, nt2s = wfst[start][mid], wfst[mid][end]
                for nt1 in nt1s:
                    for nt2 in nt2s:
                        if nt1 and nt2 and (nt1, nt2) in index:
                            temp.append(index[(nt1, nt2)])
            wfst[start][end] = list(set(temp))
    return wfst


def display(wfst, tokens):
    """Updates non-diagonal elements of chart

    Arguments:
    ---------
        wfst
        tokens (list):
            List of words in input sentence
    """
    print('\nWFST ' + ' '.join(("%-4d" % i) for i in range(1, len(wfst))))
    for i in range(len(wfst)-1):
        print("%d   " % i, end=" ")
        for j in range(1, len(wfst)):
            print("%-4s" % (wfst[i][j] or '.'), end=" ")
        print()



# MAIN FUNCTION
groucho_grammar1 = nltk.CFG.fromstring("""
    S -> NP VP
    PP -> P NP
    NP -> Det N | Det N PP | 'I'
    VP -> V NP | VP PP
    Det -> 'an' | 'my'
    N -> 'elephant' | 'pajamas'
    V -> 'shot'
    P -> 'in'
    """)

groucho_grammar2 = nltk.CFG.fromstring("""
    S -> NP VP
    PP -> P NP
    NP -> Det N | Det X | 'I'
    X -> N PP
    VP -> V NP | VP PP
    Det -> 'an' | 'my'
    N -> 'elephant' | 'pajamas'
    V -> 'shot'
    P -> 'in'
    """)

tokens = "I shot an elephant in my pajamas".split()
initial_wfst = init_wfst(tokens, groucho_grammar2)
print('Displaying Initial Chart Parser Table for Groucho Grammar...')
display(initial_wfst, tokens)

final_wfst = complete_wfst(initial_wfst, tokens, groucho_grammar2)
print('Displaying Complete Chart Parser Table for Groucho Grammar...')
display(final_wfst, tokens)
