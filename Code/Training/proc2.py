#extract only TO lines, and from those only the MATCHSTATE part

import sys

p = sys.argv[1]
if p=='2': p='o2/'
elif p=='3': p='o3/'
elif p=='4': p='o4/'
elif p=='5': p='o5/'
elif p=='6': p='o6/'
else: p='-10'

fiList = ['xaa3','xab3','xac3','xad3']

for fi in fiList:
	fName = fi
	fi = open(p+fName, 'r')
	fi2 = open(p+fName[:-1], 'r')
	fo = open(p+fName[0:-1]+'4', 'w')
	fo2 = open(p+fName[0:-1]+'5', 'w')

	for line in fi:
		line2 = fi2.readline()
		if 'uh oh' not in line:
			fo.write(line)
			fo2.write(line2)
	fi.close()
	fo.close() 
	fi2.close()
	fo2.close()
