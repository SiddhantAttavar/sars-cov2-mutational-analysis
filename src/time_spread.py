import pandas as pd
from sys import argv
from matplotlib import pyplot as plt
import matplotlib
import json
import seaborn as sns

df = pd.read_csv(argv[1], parse_dates=['Release_Date', 'Collection_Date'])
df['Collection_Date'] = pd.to_datetime(df['Collection_Date'], format='mixed')

with open(argv[2], 'r') as file:
	data = json.loads(file.read())

lineage_to_variant = {}
variant_classification = {'Other': 'No classification'}
classification_map = {
	'Variant of Interest': 'VOI',
	'Previously Circulating Variant of Concern': 'VOC',
	'Variant under Monitoring': 'VuM',
	'De-escalated': 'VOI'
}
for variant in data:
	if variant['variantType'] not in classification_map:
		continue

	variant_type = classification_map[variant['variantType']]
	variant_classification[variant['who_name']] = variant_type
	print(variant_type, variant['who_name'], len(variant['pango_sublineages']))
	if type(variant['pangolin_lineage']) == str:
		lineage_to_variant[variant['pangolin_lineage']] = variant['who_name']
	else:
		variant['pango_sublineages'] += variant['pangolin_lineage']
	for lineage in variant['pango_sublineages']:
		lineage_to_variant[lineage] = variant['who_name']
	# out_file.write(f'{variant_type},{}')

df['Variant'] = df['Pangolin'].apply(lambda x: lineage_to_variant.get(x, 'Other'))

colors = sns.color_palette('Set1') + sns.color_palette('Set2')
cmap = {}
with open(argv[3], 'r') as file:
	for i, r in enumerate(file.readlines()[1:]):
		cmap[r.split(',')[0]] = colors[i]
print(df)

matplotlib.rc('font', size = 20)
full_range = pd.date_range(start=df['Collection_Date'].min(), end=df['Collection_Date'].max())
for variant, data in df.groupby(['Variant']):
	if variant[0] not in cmap:
		continue
	counts = data['Collection_Date'].value_counts().sort_index()
	counts = counts[2:]
	counts = counts.reindex(full_range, fill_value=0)
	counts = counts.T.rolling(window = 15, min_periods = 1).mean().T
	plt.plot(counts.index, counts.values, label = variant, color = cmap[variant[0]])
plt.legend()
plt.xlabel('Collection Date')
plt.ylabel('Sequences')
plt.title(argv[4])
plt.show()
