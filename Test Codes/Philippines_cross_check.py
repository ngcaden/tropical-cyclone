import matplotlib.pyplot as plt
import numpy as np

bins = np.arange(7,19,2)

records = [10,39,71,60,81,108]

plt.bar(bins,records)

plt.show()