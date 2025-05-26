import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV
df = pd.read_csv("data/sequences.csv")

# Parse Collection_Date
df['Collection_Date'] = pd.to_datetime(df['Collection_Date'], errors='coerce')

# Drop rows with invalid dates
df = df.dropna(subset=['Collection_Date'])

# Extract month
df['month'] = df['Collection_Date'].dt.to_period('M').dt.to_timestamp()

# Optional: map pango lineages to broader variant categories
def map_variant(lineage):
    if pd.isna(lineage):
        return 'Unknown'
    lineage = lineage.upper()
    if lineage.startswith('B.1.1.7'):
        return 'Alpha'
    elif lineage.startswith('B.1.351'):
        return 'Beta'
    elif lineage.startswith('P.1'):
        return 'Gamma'
    elif lineage.startswith('B.1.617.2') or lineage.startswith('AY'):
        return 'Delta'
    elif lineage.startswith('BA') or lineage.startswith('BQ') or lineage.startswith('XBB') or lineage.startswith('EG') or lineage.startswith('JN'):
        return 'Omicron'
    else:
        return 'Other'

df['variant'] = df['Pangolin'].apply(map_variant)

# Group by month and variant
variant_counts = df.groupby(['month', 'variant']).size().unstack(fill_value=0)

# Plot
variant_counts.plot(kind='line', marker='o', figsize=(12, 6))
plt.title("COVID-19 Variant Distribution Over Time")
plt.xlabel("Collection Month")
plt.ylabel("Number of Submissions")
plt.legend(title="Variant", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
