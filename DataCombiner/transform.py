import os
import argparse
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import glob
import shutil

# Parse arguments
parser = argparse.ArgumentParser(description='Data Combiner for PPG-DaLiA dataset')
parser.add_argument('--in-directory', type=str, required=True, help="Path to the directory containing the transformed Parquet files")
parser.add_argument('--out-directory', type=str, required=True, help="Path to save the combined dataset")
parser.add_argument('--dataset-name', type=str, default='combined_dataset.parquet', help="Name of the output combined dataset file")
args = parser.parse_args()

# Check input and output directories
if not os.path.exists(args.in_directory):
    print(f"Input directory {args.in_directory} does not exist.", flush=True)
    exit(1)

if not os.path.exists(args.out_directory):
    os.makedirs(args.out_directory)

# Find all transformed Parquet files in the input directory
parquet_files = glob.glob(os.path.join(args.in_directory, '**', 'unified_data.parquet'), recursive=True)

if not parquet_files:
    print("No Parquet files found to combine.", flush=True)
    exit(1)

combined_data = []

for file_path in parquet_files:
    # Read Parquet file
    table = pq.read_table(file_path)
    df = table.to_pandas()
    
    # Read metadata from ei-metadata.json if it exists
    metadata_file = os.path.join(os.path.dirname(file_path), 'ei-metadata.json')
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            ei_metadata = json.load(f)
            metadata = ei_metadata.get('metadata', {})
            # Add metadata as columns to the dataframe
            for key, value in metadata.items():
                df[key] = value
    else:
        print(f"No metadata found for {file_path}.", flush=True)
    
    combined_data.append(df)

# Concatenate all dataframes
if combined_data:
    combined_df = pd.concat(combined_data, ignore_index=True)
    # Save combined dataframe as Parquet file
    out_file = os.path.join(args.out_directory, args.dataset_name)
    table = pa.Table.from_pandas(combined_df)
    pq.write_table(table, out_file)
    print(f'Written combined dataset to {out_file}', flush=True)
else:
    print("No data to combine after processing.", flush=True)
