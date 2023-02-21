from rsc.utils import read_results
import matplotlib.pyplot as plt
from glob import glob

file_path = glob("./results/DefaultParams_*/*h5")[0]
df = read_results(file_path)

plt.plot(df.t, df.initial, label='initial')
plt.plot(df.t, df.amorphus, label='amorphus')
plt.plot(df.t, df.nucleated, label='nucleated')
plt.plot(df.t, df.active, label='active')
plt.legend()

plt.show()
