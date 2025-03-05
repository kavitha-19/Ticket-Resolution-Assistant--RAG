import pandas as pd

# Define file paths
file1 = "dataset-tickets-multi-lang-4-20k.csv"
file2 = "dataset-tickets-multi-lang3-4k.csv"
output_file = "merged_output.csv"

# Read both Excel files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Add 'business_type' column to df1 with NaN (or any default value)
df1['business_type'] = None  # You can also use an empty string: ''

# Reorder columns to match the structure
desired_columns = ['subject', 'body', 'answer', 'type', 'queue', 'priority', 'language', 'business_type',
                   'tag_1', 'tag_2', 'tag_3', 'tag_4', 'tag_5', 'tag_6', 'tag_7', 'tag_8']

# Reorganize both DataFrames to have the same column order
df1 = df1[desired_columns]
df2 = df2[desired_columns]

# Merge the DataFrames
merged_df = pd.concat([df1, df2], ignore_index=True)

# Save the merged DataFrame to a new Excel file
# Save the merged DataFrame as a CSV file
merged_df.to_csv(output_file, index=False)

print(f"Files merged successfully into {output_file}")

