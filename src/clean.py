from Bio import AlignIO, Align
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from sys import argv

alignment = AlignIO.read(argv[1], 'fasta')

chars = 'ATCG-'
new_records = []
for i, seq in enumerate(alignment):
	if (i + 1) % 100 == 0:
		print(f'Seq: {i + 1}')
	new_seq_list = []
	for c in seq:
		if c in chars:
			new_seq_list.append(c)
		else:
			new_seq_list.append('-')
	new_seq_str = ''.join(new_seq_list)
	new_seq = SeqRecord(Seq(new_seq_str),
		id = seq.id,
		name = seq.name
	)
	new_records.append(new_seq)

new_alignment = Align.MultipleSeqAlignment(new_records)
out_file = open(argv[2], 'w')
AlignIO.write(new_alignment, out_file, 'fasta')
