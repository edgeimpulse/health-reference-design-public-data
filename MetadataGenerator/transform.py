import os
import argparse
import glob
import json

# Parse arguments
parser = argparse.ArgumentParser(description='Metadata Generator for PPG-DaLiA data')
parser.add_argument('--in-directory', type=str, required=True, help="Path to the directory containing the quest CSV file")
parser.add_argument('--out-directory', type=str, required=True, help="Path to save the metadata JSON file")
args = parser.parse_args()

# Check input and output directories
if not os.path.exists(args.in_directory):
    print(f"Data directory {args.in_directory} does not exist.", flush=True)
    exit(1)

if not os.path.exists(args.out_directory):
    os.makedirs(args.out_directory)

# Function to extract metadata from S*_quest.csv
def extract_metadata(args):
    metadata = {}
    # Find the quest file
    quest_files = sorted(glob.glob(os.path.join(args.in_directory, 'S*_quest.csv')))
    if not quest_files:
        print("No quest files found for metadata extraction.", flush=True)
        return metadata
    quest_file = quest_files[0]
    print(f"Reading metadata from {quest_file}", flush=True)
    with open(quest_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                continue  # Skip lines that don't start with '#'
            line = line.lstrip('#').strip()  # Remove '#' and any leading/trailing whitespace
            if not line or ',' not in line:
                continue
            key_value = line.split(',', 1)
            key = key_value[0].strip().lower().replace(' ', '_')
            value = key_value[1].strip()
            metadata[key] = value
            print(f"Extracted metadata - {key}: {value}", flush=True)
    # Add subject_id if not already in metadata
    if 'subject_id' not in metadata:
        subject_id = os.path.basename(args.in_directory)
        metadata['subject_id'] = subject_id
        print(f"Added subject_id: {subject_id}", flush=True)
    return metadata

# Extract metadata
metadata = extract_metadata(args)

# Debug: Print metadata
print(f"Extracted metadata: {metadata}", flush=True)

# Check if metadata is empty
if not metadata:
    print("No metadata extracted. Metadata will be empty in ei-metadata.json.", flush=True)

# Create ei-metadata.json
ei_metadata = {
    "version": 1,
    "action": "add",
    "metadata": metadata
}

# Write ei-metadata.json to the output directory
metadata_file = os.path.join(args.out_directory, 'ei-metadata.json')
with open(metadata_file, 'w') as f:
    json.dump(ei_metadata, f)

print(f'Written metadata file: {metadata_file}', flush=True)
