import numpy as np 
import os
import pandas as pd
from datetime import datetime
from mpl_toolkits.basemap import Basemap

script_directory = os.path.dirname(os.path.abspath(__file__))
print(script_directory)

script_directory = os.path.dirname(script_directory)
script_directory = os.path.join(script_directory, "Dataset", "Raw_dataset")

print(script_directory)

# Explore the different directory

for path_it in os.listdir(script_directory):

    path = os.path.join(script_directory, path_it, "raw")
    # Handle the .csv file
    
    for file in os.listdir(path):
        if file.endswith('.csv'):
            csv_path = os.path.join(path, file)

            # Converting the time format from PIGEON3 into the same as the other
            if "PIGEON3" in csv_path:
                df = pd.read_csv(csv_path)
                print("path", csv_path)

                # Print the column names to verify
                print("Column names:", df.columns)

                # Strip any leading/trailing spaces from the column names
                df.columns = df.columns.str.strip()

                # Check for 'LOCAL DATE' and 'LOCAL TIME' columns
                if 'LOCAL DATE' in df.columns and 'LOCAL TIME' in df.columns:
                    date_time_str = df['LOCAL DATE'] + ' ' + df['LOCAL TIME']
                    
                    # Try parsing with multiple formats
                    try:
                        df['time'] = pd.to_datetime(date_time_str, format='%d/%m/%Y %H:%M:%S')
                    except ValueError:
                        try:
                            df['time'] = pd.to_datetime(date_time_str, format='%Y/%m/%d %H:%M:%S')
                        except ValueError:
                            print("Error parsing date and time for file:", csv_path)
                            continue
                    
                    # Format datetime objects to desired format
                    df['time'] = df['time'].dt.strftime("%Y-%m-%d %H:%M:%S.%f")

                    # Parameters depending on the file
                    long_param = 'LONGITUDE'
                    lat_param = 'LATITUDE'
                    z_param = 'ALTITUDE'

                    # Create a Basemap instance
                    lat = df[lat_param]
                    long = df[long_param]
                    z = df[z_param]
                    m = Basemap(projection='merc', llcrnrlat=lat.min(), urcrnrlat=lat.max(), llcrnrlon=long.min(), urcrnrlon=long.max(), resolution='c')
                    x, y = m(long.values, lat.values)

                    # Create a new dataset
                    new_df = pd.DataFrame({'time': df['time'], 'x': x, 'y': y, 'z': z})
                    path_output = os.path.dirname(os.path.abspath(__file__))
                    path_output = os.path.dirname(path_output)
                    path_output = os.path.join(path_output, "Dataset", "Raw_trajectories", "PIGEON3", "Data_processed", file)
                    print("output", path_output)
                    new_df.to_csv(path_output, index=False, header=True)
                else:
                    print("Error: 'LOCAL DATE' or 'LOCAL TIME' column is missing in file:", csv_path)
