import numpy as np
import dill
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import seaborn as sns
import os

# %%

fileNum = -1
dir_path='result'
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        fileNum +=1

exper = [0 for _ in range(fileNum)]
for i in range(5):
    with open(f"result/Result_p0_r{i}_Sheet1.pkl", "rb") as f:
        exper[i] = dill.load(f)

print([i['fidelity'] for i in exper])