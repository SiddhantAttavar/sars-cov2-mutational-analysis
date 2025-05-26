import pandas as pd
import numpy as np
from sys import argv
from matplotlib import pyplot as plt

data = pd.read_csv(argv[1])
nucleotides = data.columns[1:]
positions = data['Col']

data[nucleotides] = data[nucleotides].apply(pd.to_numeric)

fig, ax = plt.subplots(figsize=(12, 6))

bottom = np.zeros(len(positions))

for nuc in nucleotides:
	ax.bar(positions, data[nuc], bottom=bottom, label=nuc, alpha=0.8)
	bottom += data[nuc]

ax.set_xlabel("Alignment Position")
ax.set_ylabel("Relative Frequency")
ax.set_title("Nucleotide Frequency Distribution Across Alignment")
ax.legend(title="Nucleotide")

plt.savefig(argv[2])
