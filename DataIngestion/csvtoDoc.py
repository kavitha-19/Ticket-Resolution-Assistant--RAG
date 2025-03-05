import csv
import json

# Input and output file paths
input_csv = 'dataset_with_ID.csv'
output_folder = 'json_docs'

# Create output folder if it doesn't exist
import os
os.makedirs(output_folder, exist_ok=True)

# Read CSV and convert each row into a document
with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for i, row in enumerate(reader):
        document = {
            "ID": row['id'],
            "Subject": row['subject'],
            "Body": row['body'],
            "Answer": row['answer'],
            "Type": row['type'],
            "Queue": row['queue'],
            "Priority": row['priority'],
            "Language": row['language'],
            "Business Type": row['business_type'],
            "Tags": [row[tag] for tag in ['tag_1', 'tag_2', 'tag_3', 'tag_4', 'tag_5', 'tag_6', 'tag_7', 'tag_8'] if row[tag]]
        }
        # Write each document as a JSON file
        output_path = os.path.join(output_folder, f'document_{i+1}.json')
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(document, json_file, indent=4)

print(f"Documents have been created in the '{output_folder}' folder.")
