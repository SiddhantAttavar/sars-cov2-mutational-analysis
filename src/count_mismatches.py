from Bio import AlignIO
from sys import argv
from collections import Counter, defaultdict
from multiprocessing import Process
import json

alignment = AlignIO.read(argv[1], 'fasta')
length = alignment.get_alignment_length()
count_mismatches = defaultdict(lambda: [0] * length)

def count(l, r):
	global count_mismatches
	for i in range(l, r):
		counter = Counter(alignment[:, i])
		if i % 100 == 0:
			print(f'Column: {i}')
		for k, v in counter.items():
			for x, y in counter.items():
				if k < x:
					count_mismatches[k+x][i] = v * y

t = int(argv[3])
k = length // t

threads = [Process(target = count, args = (i * k, i * k + k)) for i in range(t - 1)]
threads.append(Process(target = count, args = ((t - 1) * k, length)))

for thread in threads:
	thread.start()

for thread in threads:
	thread.join()

print(f'Mismatch count: {count_mismatches}')
output_file = open(argv[2], 'w')
output_file.write(json.dumps(count_mismatches))
output_file.close()
