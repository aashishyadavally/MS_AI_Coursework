"""
Name: Aashish Yadavally
"""

def tdhstep(g, input_categories_history): # Compute all possible next steps from (i, cs)
    (i, cs, h) = input_categories_history
    if len(cs) > 0:
        cs1 = cs[1:] # copy of predicted categories except cs[0]
        nextsteps = []
        for index, (lhs, rhs) in enumerate(g):
            if lhs == cs[0]:
                #print('expand', lhs,'->',rhs)  # for trace
                h1 = h[:] # copy of history
                h1.append((i, rhs + cs1))
                nextsteps.append((i, rhs + cs1, h1))
        if len(i) > 0 and i[0] == cs[0]:
            #print('scan', i[0]) # for trace
            i1 = i[1:]
            h1 = h[:] # copy of history
            h1.append((i1,cs1))
            nextsteps.append((i1, cs1, h1))
        return nextsteps
    else:
        return []

def derive(g, ds):
    derivations = []
    rv = []
    while ds != [] and not (ds[-1][0] == [] and ds[-1][1] == []):
        d = ds.pop()        
        x = tdhstep(g, d)
        ds.extend(x)
        if len(x) != 0:
            current = x[-1][0] + x[-1][1]
            rv.append([current, len(ds)])        
    return rv
            

def parse(g, i):
    ds = [(i, ['S'], [(i, ['S'])])]
    while ds != []:
        rv = derive(g, ds)
        if ds == []:
            return 'False'
        else:
            d = ds.pop()
            current = i[0] + i[1]
            print(current)
            for n, step in enumerate(d[2]):
                if n == 0:
                    bt_steps = 1
                else:
                    bt_steps = get_bt_steps(rv, current)
                print(n, len(step[1]), bt_steps, step)
            ans = input('more? ')
            if len(ans) > 0 and ans[0] == 'n':
                return d[2]

def get_bt_steps(rv, current):
    for (pos, steps) in rv:
        if pos == current:
            return steps


# Examples:
# parse(g1,['Sue','laughs'])
# parse(g1,['the','student','laughs'])
# parse(g1,['the','student','praises','the','beer'])
# parse(g1,['Bill','knows','Sue','laughs'])
# parse(g1, ['two','wine','from','her','knows','the','wine','knows','her','knows'])

#################################################################################################
# Q3.  (a) The highest the value of 'n' can get is '3', i.e, the parser memory can have 
#          a maximum of 3 elements at any point in calculating one of its parses. An
#          example of a sentence which requires the most parser memory is:
#          " two wine from her knows the wine knows her knows "
#
#      (b) Top-down parser follows left-to-right, leftmost derivation. The maximum number
#          of elements on the right side of the derivation rules in the grammar is 3,
#          because of which, while moving from the leftmost non-terminal to the right,
#          there can not be more than 3 elements in the parser memory.
#
#      (c) The sentence described above, i.e, " two wine from her knows the wine knows her knows "
#          requires more backtrack memory (which is 66 in this case). 
#
#      (d) In order to maximize the number of derivations elements in the backtrack stack,
#          such rules were chosen which led to more non-terminals, and when the terminals
#          were chosen, such ones were chosen which were at the end of the grammar for
#          that particular non-terminal. This led to an increase in the number of
#          derivation elements in the backtrack stack.    
#

