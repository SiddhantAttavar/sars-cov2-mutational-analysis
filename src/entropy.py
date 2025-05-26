from Bio import AlignIO
from sys import argv
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math

def shannon_entropy(column):
    """Calculate Shannon entropy for a given column of MSA."""
    counts = Counter(column)
    total = sum(counts.values())
    entropy = -sum((count / total) * math.log2(count / total) for count in counts.values() if count > 0)
    return entropy

def identify_hotspots(msa_file, threshold=0.9):
    """Identify mutational hotspots from an MSA file using Shannon entropy."""
    alignment = AlignIO.read(msa_file, "fasta")
    num_positions = alignment.get_alignment_length()
    print(len(alignment), num_positions)
    
    # Compute entropy for each column
    entropy_values = [shannon_entropy(alignment[:, i]) for i in range(num_positions)]
    
    # Determine hotspot threshold (e.g., top 10% most variable positions)
    cutoff = np.percentile(entropy_values, threshold * 100)
    hotspots = [i for i, e in enumerate(entropy_values) if e >= cutoff]

    return entropy_values, hotspots

def plot_hotspots(entropy_values, hotspots):
    """Plot entropy values with hotspots highlighted."""
    plt.figure(figsize=(12, 6))
    plt.plot(entropy_values, label="Shannon Entropy", color='blue')
    plt.scatter(hotspots, [entropy_values[i] for i in hotspots], color='red', label="Hotspots")
    plt.xlabel("Position in Alignment")
    plt.ylabel("Shannon Entropy")
    plt.title("Mutational Hotspots in MSA")
    plt.legend()
    plt.show()

# Run analysis
msa_file = argv[1]  # Replace with your actual MSA file
entropy_values, hotspots = identify_hotspots(msa_file)
print(f"Identified hotspots at positions: {hotspots}")

# Plot results
plot_hotspots(entropy_values, hotspots)
