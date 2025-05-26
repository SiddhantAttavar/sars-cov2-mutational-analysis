import os
from sys import argv
import subprocess
import pandas as pd
from matplotlib import pyplot as plt

def get_plot(file_name, title):
	df = pd.read_csv(file_name)
	plt.plot(df['Entropy'])
	plt.title(title)
	plt.xlabel('Alginment column')
	plt.ylabel('Entropy')

for file in os.listdir(argv[1]):
	if not file.endswith('.fasta'):
		continue
	file_name = file.rstrip('.fasta')
	subprocess.run(['./count_mismatches', f'{argv[1]}/{file}', f'{argv[1]}/{file_name}.csv'])
	subprocess.run(['./entropy', f'{argv[1]}/{file_name}.fasta', f'{argv[1]}/{file_name}_hotspots.csv'])
	get_plot(f'{argv[1]}/{file_name}_entropy.csv', f'{file_name} Mutational Entropy')
	plt.savefig(f'{argv[1]}/{file_name}.png')
	plt.show()
