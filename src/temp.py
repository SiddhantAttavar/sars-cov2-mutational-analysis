from csv import csv_reader
import numpy as np
from matplotlib import pyplot as plt
from sys import argv

data = list(csv_reader(open(argv[1])))

chars = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
l = [(i, r) for i, r in enumerate(data[0]) if r[0] in chars and r[1] in chars]

out_folder = argv[2]
cols = list(map(int, argv[3].split(',')))
data = [data[i - 1] for i in cols]
print(data)

for row in data:
	mat = np.ones(((len(chars), len(chars))), 'int64')
	for i, (a, b) in l:
		print(i, a + b, row[i])
		mat[chars[a], chars[b]] += int(row[i])
	print(mat)
	mat = np.log(mat)
	plt.matshow(mat, cmap = 'hot')
	plt.savefig(f'{out_folder}/col{int(row[0]) + 1}.png')
	plt.show()
