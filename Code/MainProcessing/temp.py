import numpy as np
import pickle as pk

cumulative = []
for i in range(24):
    temp = np.load('Package/fiveHands'+str(i)+'.pickle',allow_pickle=True)
    cumulative += temp
   
with open('Package/fiveHands.pickle', 'wb') as f:
    pk.dump(cumulative, f, protocol=pk.HIGHEST_PROTOCOL)