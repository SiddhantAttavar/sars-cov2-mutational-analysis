from json import loads
from sys import argv
from csv import reader
from Bio import AlignIO, Align
from collections import defaultdict

with open(argv[1], 'r') as file:
	map_data = defaultdict(lambda: {'wholabel': 'Other'}, loads(file.read()))

acc_id_to_voc = {}
voc_to_lineage = defaultdict(lambda: set())
with open(argv[2], 'r') as csv_file:
	csv_reader = reader(csv_file)
	next(csv_reader)
	for row in csv_reader:
		variant = map_data[row[8]]['wholabel']
		acc_id_to_voc[row[0]] = variant
		# acc_id_to_voc[row[0]] = row[8]
		voc_to_lineage[variant].add(row[8])
		# acc_id_to_vc[row[0]] = map_variant(row[8])

for k, v in voc_to_lineage.items():
	print(k, v)
print()

alignment = AlignIO.read(argv[3], 'fasta')
new_records = {}
for i, seq in enumerate(alignment):
	acc_id = seq.name.split('|')[0].lstrip('>').rstrip()
	if acc_id not in acc_id_to_voc:
		continue
	voc = acc_id_to_voc[acc_id]
	if voc not in new_records:
		new_records[voc] = []
	new_records[voc].append(seq)

print(f'Total: {sum([len(i) for i in new_records.values()])}')
for k, v in new_records.items():
	print(f'VOC: {k}: {len(v)}')

for voc, seqs in new_records.items():
	out_alignment = Align.MultipleSeqAlignment(seqs)
	with open(f'{argv[4]}/{voc}.fasta', 'w') as out_file:
		AlignIO.write(out_alignment, out_file, 'fasta')
