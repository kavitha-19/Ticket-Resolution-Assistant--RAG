import pandas as pd

# Load the CSV file
df = pd.read_csv("./archive/merged_output.csv")

# Add an auto-incremented unique ID column
df.insert(0, "id", range(1, len(df) + 1))

# Save the modified CSV file
df.to_csv("dataset_with_ID.csv", index=False)

print("CSV file updated successfully with unique ID!")
