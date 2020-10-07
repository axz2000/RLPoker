import numpy as np
import pickle as pk

def remDups(cNum):
    x = np.load('x'+str(cNum)+'.pickle',allow_pickle=True)
    y = np.load('y'+str(cNum)+'.pickle',allow_pickle=True)
    print("Data Loaded")
    
    unique_rows, idxs = np.unique(x, axis=0, return_index=True)
    print("Uniques Found")
    ya = np.asarray(y)
    ya = ya[idxs]
    
    if (ya.shape[0]!=unique_rows.shape[0]): 1/0
    print("Check Passed")
    
    with open('finalx'+str(cNum)+'.pickle', 'wb') as f:
        pk.dump(unique_rows, f, protocol=pk.HIGHEST_PROTOCOL)
        print("X Written")
    with open('finaly'+str(cNum)+'.pickle', 'wb') as f:
        pk.dump(ya, f, protocol=pk.HIGHEST_PROTOCOL)
        print("Y Written")
        
        
remDups(7)
remDups(6)
remDups(5)
remDups(2)