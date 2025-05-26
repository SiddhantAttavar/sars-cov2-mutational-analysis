from sys import argv
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib

colors = sns.color_palette("tab20") + sns.color_palette("Set3", 10)
regions = pd.read_csv(argv[2])
def get_plot(file_name, title):
	matplotlib.rc('font', size = 20)
	fig, ax = plt.subplots()
	ax.plot(df['Total'])
	ax.set_title(title)
	ax.set_xlabel('Alignment column')
	ax.set_ylabel('Mismatches')
	for i, (region, start, end) in regions.iterrows():
		ax.axvspan(start, end, facecolor = colors[i], alpha = 0.5, zorder = -1, label = region)
	# ax.legend(regions['Color'], regions['Region'])
	matplotlib.rc('font', size = 12)
	ax.legend()
	ax.set_xlim([0, 40000])
	ax.grid(True)
	plt.ylim([0, int(2.5e6)])
	plt.show()

df = pd.read_csv(argv[1])
get_plot(df, 'Mismatch count')
