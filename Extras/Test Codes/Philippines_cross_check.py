import matplotlib.pyplot as plt
import numpy as np

bins = np.arange(6,18,2)

records = [6,22,48,35,39,55]

plt.bar(bins,records,width=2)

plt.show()