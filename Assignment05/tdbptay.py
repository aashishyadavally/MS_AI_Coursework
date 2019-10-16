""" 
Name: Aashish Yadavally
"""
import heapq


g4 = [('S',['a','S','S']),
      ('S',[])]


def tdpstep(g, input_categories_parses): # compute all possible next steps from (ws,cs)
    global n_steps
    (ws,cs,p) = input_categories_parses
    if len(cs)>0:
        cs1=cs[1:] # copy of predicted categories except cs[0]
        p1 = p[:]  # copy of rules used so far
        nextsteps=[]
        for (lhs,rhs) in g:
            if lhs == cs[0]:
                n_steps += 1
                print('expand',lhs,'->',rhs)  # for trace
                nextsteps.append((ws,rhs+cs1,p1+[[lhs]+rhs]))
        if len(ws)>0 and ws[0] == cs[0]:
            n_steps += 1
            print('scan',ws[0]) # for trace
            ws1=ws[1:]
            nextsteps.append((ws1,cs1,p1))
        return nextsteps
    else:
        return []

def derive(g,beam,k):
    global n_steps
    while beam != [] and not (min(beam)[1] == [] and min(beam)[2] == []):
        (prob0,ws0,cs0,p0) = heapq.heappop(beam)
        nextsteps = tdpstep(g,(ws0,cs0,p0))
        print('nextsteps=',nextsteps)
        if len(nextsteps) > 0:
            prob1 = prob0/float(len(nextsteps))
            if -(prob1) > k:
                for (ws1,cs1,p1) in nextsteps:
                    n_steps += 1
                    heapq.heappush(beam,(prob1,ws1,cs1,p1))
                    print ('pushed',(prob1,ws1,cs1)) # for trace
        print('|beam|=',len(beam)) # for trace

def parse(g,ws,k):
    global n_steps
    n_steps = 0
    beam = [(-1.,ws,['S'],[])]
    heapq.heapify(beam) # make list of derivations into a "min-heap"
    while beam != []:
        derive(g,beam,k)
        if beam == []:
            return 'False'
        else:
            d=heapq.heappop(beam)
            print('ll=', d[3])
            print('Number of steps are: ' +  str(n_steps))
#            ans = input('another? ')
#            if len(ans)>0 and ans[0]=='n':
#                return d[3]

# parse(g4, list('a'), 0.0001)
# parse(g4, list('aa'), 0.0001)
# parse(g4, list('aaa'), 0.0001)
# parse(g4, list('aaaa'), 0.0001)
# parse(g4, list('aaaaa'), 0.0001)
# parse(g4, list('aaaaaa'), 0.0001)
# parse(g4, list('aaaaaaa'), 0.0001)

############################################################################################
# 	3. Number of steps to parse 'a': 14
#	   Number of steps to parse 'aa': 38
# 	   Number of steps to parse 'aaa': 104
# 	   Number of steps to parse 'aaaa': 300 
#	   Number of steps to parse 'aaaaa': 912 
#	   Number of steps to parse 'aaaaaa': 2892
# 	   Number of steps to parse 'aaaaaaa': 6896
#
#	4. For all values of 'n' greater than or equal to 1, the number of steps required
#          to find all parses of the sentence exceed 2^n. 
#
#

