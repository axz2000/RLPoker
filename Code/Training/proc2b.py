
fName = 'dealerOutput_v4.txt'
fName2 = 'dealerOutput_v2.txt'
fi = open(fName, 'r')
fi2 = open(fName2, 'r')
fo = open('dealerOutput_v5.txt', 'w')
fo2 = open('dealerOutput_v6.txt', 'w')

for line in fi:
	line2 = fi2.readline()
	if 'uh oh' not in line:
		fo.write(line)
		fo2.write(line2)
fi.close()
fo.close() 
fi2.close()
fo2.close()
