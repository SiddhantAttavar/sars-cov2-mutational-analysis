import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sys import argv

df = pd.read_csv(argv[1])

chars = {}
for a, b in df.columns[1:]:
	if a not in chars:
		chars[a] = len(chars)
	if b not in chars:
		chars[b] = len(chars)
chars = {'A': 0, 'C': 1, 'T': 2, 'G': 3}

out_folder = argv[2]
# cols = list(map(int, argv[3].split(',')))
# df = df.take(cols)

l = [(i, r) for i, r in enumerate(df.columns[1:]) if r[0] in chars and r[1] in chars]
for col, row in df.iterrows():
	mat = np.ones(((len(chars), len(chars))), 'int64')
	print(list(row))
	for i, (a, b) in l:
		mat[chars[a], chars[b]] += row[i]
	print(mat)
	mat = np.log(mat)
	plt.imshow(mat, cmap = 'hot')
	plt.savefig(f'{out_folder}/col{col}.png')
	# plt.show()
