from json import loads
from sys import argv
from csv import reader, writer

with open(argv[1], 'r') as file:
	data = loads(file.read())

variants = []
classification_map = {
	'Variant of Interest': 'VOI',
	'Previously Circulating Variant of Concern': 'VOC',
	'Variant under Monitoring': 'VuM',
	'De-escalated': 'VOI'
}

# out_file = open(argv[2], 'w')
# out_file.write('Variant Classification,WHO Name,Number of sublineages,Number of sublineages')
lineage_to_variant = {}
variant_classification = {'Other': 'No classification'}
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

print()
sublineages = {}
variant_count = {}
with open(argv[2], 'r') as csv_file:
	csv_reader = reader(csv_file)
	next(csv_reader)
	for row in csv_reader:
		variant = lineage_to_variant.get(row[8], 'Other')
		if variant not in sublineages:
			sublineages[variant] = set()
			variant_count[variant] = 0
		# if variant == 'Other':
		# 	print(row[8])
		sublineages[variant].add(row[8])
		variant_count[variant] += 1

rows = []
for k, v in sublineages.items():
	if k == None:
		continue
	print(variant_classification[k], k, len(v))
	rows.append([k, variant_classification[k], variant_count[k], ', '.join(v)])
ordering = ['VOC', 'VOI', 'VuM', 'No classification']
rows.sort(key = lambda x: ordering.index(x[1]))

with open(argv[3], 'w') as csv_file:
	csv_writer = writer(csv_file)
	csv_writer.writerow(['WHO name', 'Variant classification', 'Sequence count', 'Sublineages'])
	csv_writer.writerows(rows)

