import nltk

def demo(grammar,sent):
    tokens = sent.split()
    cp = nltk.parse.FeatureChartParser(grammar, trace=1)
    chart = cp.chart_parse(tokens)
    trees = list(chart.parses(grammar.start()))
    treecount = 0
    for tree in trees:
        print(tree)
        treecount += 1
    print('{} trees'.format(treecount))

german = nltk.data.load('german.fcfg')
demo(german, 'ich komme den Katzen')
