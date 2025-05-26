# sars-cov2-mutational-analysis
This repository contains the code for my study project (BIO-F266) on "Identification of mutational hotspots in SARS-Cov-2 genome sequences". There are a total of 8 scripts used for the analysis and identification of mutational hotspots.

## Script usage:
### Computational scripts:
1. Alignment cleaning (`clean.py`): <br>
	`python3 clean.py raw_alignment.fasta cleaned_alignment.fasta`
2. Count mismatches (`count_mismatches.cpp` or `count_mismatches.py`): <br>
	`g++ count_mismatches.cpp -o count_mismatches` <br>
	`./count_mismatches alignment.fasta output.csv` <br>
	**OR** (not recommended) <br>
	`python3 count_mismatches.py alignment.fasta output.json threads`
4. Calculating positional mutational entropy (`entropy.cpp`): <br>
	`g++ entropy.cpp -o entropy` <br>
	`./entropy alignment.fasta output.csv` <br>
	**OR** (not recommended) <br>
	`python3 entropy.py alignment.fasta`
4. Identify hotspots and plot positional mutational entropy (`hotspots.py`): <br>
	`python3 hotspots.py entropy.csv output.csv ref_regions.csv`

> Note: Alignment is performed with [HAlign-4](https://github.com/metaphysicser/HAlign-4) using the command <br>
> `./halign4 sequences.fasta alignment.fasta -r reference.fasta`

### Visualization scripts:
1. Generate heat maps of mismatch count (`heatmap.py`): <br>
	`python3 heatmap.py mismatch.csv out_folder`
2. Generate positional graph of mismatch frequencies (`mismatch_graph.py`): <br>
	`python3 mismatch_graph.py mismatch_count.csv ref_regions.csv`
3. Plot temporal distribution of SARS-Cov-2 variants (`time_spread.py`): <br>
	`python3 time_spread.py sequences.csv curated_lineages.json variants.csv title`
4. Generate variant statistics (`voc_statistics.py`): <br>
	`python3 voc_statistics.py curated_lineages.json sequences.csv output.csv`
