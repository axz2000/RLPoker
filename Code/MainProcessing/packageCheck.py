import numpy as np
import pickle as pk
import math

'''
x = np.load("Package/twoHands0.pickle",allow_pickle=True)
y = open("Package7/twoHands0.csv","r")

yy = y.readlines()
test = yy[0]

test = test.strip()
test = test.split(',')

numFiles = 64
prefix = 'six'
wtr = open('histo6_7.csv','w')

for i in range(numFiles):
    x = open("Package7/"+prefix+"Hands"+str(i)+".csv","r")
    x = x.readlines()
    for line in x:
        wtr.write(line)
wtr.close()'''
 


def processLine(line):
    line = line.strip()
    line = line.split(',')
    line = [int(i) for i in line]
    return {(i+1)/100:val for i,val in enumerate(line)}


def calc_percentiles(cnts_dict, percentiles_to_calc=range(101)):
    """Returns [(percentile, value)] with nearest rank percentiles.
    cnts_dict: { <value>: <count> }
    percentiles_to_calc: iterable for percentiles to calculate; 0 <= ~ <= 100
    """
    assert all(0 <= p <= 100 for p in percentiles_to_calc)
    percentiles = []
    num = sum(cnts_dict.values())
    cnts = sorted(cnts_dict.items())
    curr_cnts_pos = 0  # current position in cnts
    curr_pos = cnts[0][1]  # sum of freqs up to current_cnts_pos
    for p in sorted(percentiles_to_calc):
        if p < 100:
            percentile_pos = p / 100.0 * num
            while curr_pos <= percentile_pos and curr_cnts_pos < len(cnts):
                curr_cnts_pos += 1
                curr_pos += cnts[curr_cnts_pos][1]
            #percentiles.append((p, cnts[curr_cnts_pos][0]))
            percentiles.append(cnts[curr_cnts_pos][0])
        else:
            #percentiles.append((p, cnts[-1][0]))
            percentiles.append(cnts[-1][0])
    return percentiles

def writeHistoToPercentiles(fileName, percentileStep=10): #10th percentiles
    fi = open(fileName,'r')
    
    outName = fileName.split('/')[0]+'/percentile'+str(100//percentileStep)+'_'+fileName.split('/')[-1][5:]
    fo = open(outName,'w')
    
    for line in fi:
        line = processLine(line)
        ps = calc_percentiles(line, range(0,101,percentileStep))[:-1]
        
        fo.write(str(ps[0]))
        for val in ps[1:]:
            fo.write(','+str(val))
        fo.write('\n')
    
    fi.close()
    fo.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    