from nltk import load_parser


def check(p):
	print('{:<20}\t{:>8}'.format('example', 'analyses'))
	f = lambda s: len(list(p.parse(s.split())))
	for ex in testsuite:
		print('{:<20}\t{:>8}'.format(ex, f(ex)))

# HW8 Q2
onea = 'Juan vió algo'
oneb = 'Juan vió a algo'
twoa = 'Juan vió alguien'
twob = 'Juan vió a alguien'

testsuite = [onea, oneb, twoa, twob]

p = load_parser('spanish.fcfg', cache=False)
check(p)
