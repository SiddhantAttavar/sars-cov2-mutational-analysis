from sys import argv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib

colors = sns.color_palette("tab20") + sns.color_palette("Set3", 10)
ref_regions = pd.read_csv(argv[3])
def get_plot(file_name, title):
	matplotlib.rc('font', size = 20)
	fig, ax = plt.subplots()
	ax.plot(df['Entropy'])
	ax.set_title(title)
	ax.set_xlabel('Alignment column')
	ax.set_ylabel('Entropy (bits)')
	for i, (region, start, end) in ref_regions.iterrows():
		ax.axvspan(start, end, facecolor = colors[i], alpha = 0.5, zorder = -1, label = region)
	# ax.legend(regions['Color'], regions['Region'])
	matplotlib.rc('font', size = 12)
	ax.legend()
	ax.set_xlim([0, 40000])
	ax.grid(True)
	plt.ylim([0, 1.6])
	plt.show()

df = pd.read_csv(argv[1])
get_plot(df, 'Positional Mutation Entropy')

window = 20
mean = df['Entropy'].rolling(window = window, min_periods = 1).mean().to_numpy()
print(len(mean))
print(mean)

hotspots = np.argsort(mean)[::-1]
hotspots = hotspots[hotspots > 500]
hotspots = hotspots[hotspots < len(mean) - 500]
print(hotspots)
print(mean[hotspots])

vis = [False] * len(mean)
regions = []
for i in hotspots:
	for j in range(i, min(len(mean), i + window)):
		if vis[j]:
			break
	else:
		for j in range(i, min(len(mean), i + window)):
			vis[j] = True
		regions.append(i)

regions = np.array(regions)
hotspot_means = mean[regions]

print(regions[:100])
print(hotspot_means[:100])
print(ref_regions)

with open(argv[2], 'w') as file:
	file.write('Start,End,Avg. entropy,Region\n')
	for i in regions:
		ref = None
		curr = 0
		for _, (region, start, end) in ref_regions.iterrows():
			if start <= i + 1 and start > curr:
				ref = region
				curr = start
		file.write(f'{i + 1},{i + window},{mean[i]},{ref}\n')
	file.close()
