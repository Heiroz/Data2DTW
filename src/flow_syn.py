import pandas as pd
import os
from datetime import datetime

def process(csv_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    data = pd.read_csv(csv_path)
    
    required_columns = ['srcip', 'dstip', 'srcport', 'dstport', 'proto']
    if not all(column in data.columns for column in required_columns):
        raise ValueError("CSV file must contain the following columns: srcip, dstip, srcport, dstport, proto")
    if 'time' not in data.columns:
        raise ValueError("CSV file must contain a 'time' column for sorting")
    
    data['time'] = pd.to_datetime(data['time'], unit='us')

    grouped = data.groupby(required_columns)
    
    for name, group in grouped:
        if len(group) > 20:
            group_sorted = group.sort_values(by='time')
            filename = f"{'_'.join(map(str, name))}.csv"
            filepath = os.path.join(output_folder, filename)
            group_sorted.to_csv(filepath, index=False)