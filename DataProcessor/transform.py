import numpy as np
import os
import argparse
import pandas as pd
import pyarrow as pa
import glob
import pyarrow.parquet as pq

# Parse arguments
parser = argparse.ArgumentParser(description='Transformation block for PPG-DaLiA data processing')
parser.add_argument('--in-directory', type=str, required=True, help="Path to the directory containing the CSV files")
parser.add_argument('--out-directory', type=str, required=True, help="Path to save the transformed Parquet file")
args = parser.parse_args()

# Check input and output directories
if not os.path.exists(args.in_directory):
    print(f"Data directory {args.in_directory} does not exist.", flush=True)
    exit(1)

if not os.path.exists(args.out_directory):
    os.makedirs(args.out_directory)

# Define paths to the necessary CSV files
acc_file = os.path.join(args.in_directory, 'ACC.csv')
hr_file = os.path.join(args.in_directory, 'HR.csv')
eda_file = os.path.join(args.in_directory, 'EDA.csv')
bvp_file = os.path.join(args.in_directory, 'BVP.csv')
temp_file = os.path.join(args.in_directory, 'TEMP.csv')

# Find activity files matching 'S*_activity.csv'
activity_files = sorted(glob.glob(os.path.join(args.in_directory, 'S*_activity.csv')))
if not activity_files:
    print("No activity files found. Skipping processing.", flush=True)
    exit(1)

activity_file = activity_files[0]  # Select the first matching file

# Check if all required files are available
required_files = [acc_file, hr_file, eda_file, bvp_file, temp_file, activity_file]
for file_path in required_files:
    if not os.path.exists(file_path):
        print(f"Missing file {file_path}. Skipping processing.", flush=True)
        exit(1)

# Load data from CSV files
acc_data = pd.read_csv(acc_file, header=None, skiprows=2, names=['accX', 'accY', 'accZ'])
hr_data = pd.read_csv(hr_file, header=None, skiprows=2, names=['heart_rate'])
eda_data = pd.read_csv(eda_file, header=None, skiprows=2, names=['eda'])
bvp_data = pd.read_csv(bvp_file, header=None, skiprows=2, names=['bvp'])
temp_data = pd.read_csv(temp_file, header=None, skiprows=2, names=['temperature'])

# Load and clean activity labels
activity_labels = pd.read_csv(activity_file, header=None, skiprows=1, names=['activity', 'start_row'])
activity_labels['activity'] = activity_labels['activity'].str.strip()
activity_labels['start_row'] = pd.to_numeric(activity_labels['start_row'], errors='coerce')
activity_labels = activity_labels.dropna(subset=['start_row']).reset_index(drop=True)
activity_labels['start_row'] = activity_labels['start_row'].astype(int)

# Set default activity and map activities to rows based on start_row intervals
acc_data['activity'] = 'NO_ACTIVITY'
for i in range(len(activity_labels) - 1):
    activity = activity_labels.loc[i, 'activity']
    start_row = activity_labels.loc[i, 'start_row']
    end_row = activity_labels.loc[i + 1, 'start_row']
    acc_data.loc[start_row:end_row - 1, 'activity'] = activity

# Handle the last activity to the end of the dataset
last_activity = activity_labels.iloc[-1]['activity']
last_start_row = activity_labels.iloc[-1]['start_row']
acc_data.loc[last_start_row:, 'activity'] = last_activity

# Calculate features
acc_features = {
    'accX_rms': np.sqrt(np.mean(acc_data['accX']**2)),
    'accY_rms': np.sqrt(np.mean(acc_data['accY']**2)),
    'accZ_rms': np.sqrt(np.mean(acc_data['accZ']**2)),
}
hr_mean = hr_data['heart_rate'].mean()
eda_mean = eda_data['eda'].mean()
bvp_mean = bvp_data['bvp'].mean()
temp_mean = temp_data['temperature'].mean()

# Combine features and unique activity labels
features = {
    **acc_features,
    'heart_rate_mean': hr_mean,
    'eda_mean': eda_mean,
    'bvp_mean': bvp_mean,
    'temperature_mean': temp_mean,
    'activity_labels': [activity_labels['activity'].tolist()]  # Nest the list of activities
}

# Convert features to DataFrame and save as Parquet file
features_df = pd.DataFrame([features])
out_file = os.path.join(args.out_directory, 'unified_data.parquet')
table = pa.Table.from_pandas(features_df)
pq.write_table(table, out_file)

print(f'Written features Parquet file: {out_file}', flush=True)
