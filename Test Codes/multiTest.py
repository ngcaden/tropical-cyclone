from multiprocessing import Pool
import time
import numpy as np
from

start_time = time.time()

def f(x):
	return np.cos(x*x)

p = Pool(10)

input = list(np.arange(0,1000,0.1))

Result=p.map(f, input)
print("--- %s seconds ---" % (time.time() - start_time))