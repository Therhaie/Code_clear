import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import traceback

# Get the path to the Tools directory
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
path = os.path.join(path, "Tools")
print(path)

# Add the path to the directory containing distance.py
sys.path.append(os.path.abspath(path))

# Import the distance function
from calc_distance_from_csv import calc_distance


MIN_DISTANCE_PER_TRACK = 4000
MAX_DISTANCE_PER_TRACK = 6000

''' The purpose of this code is to delete every splitted trajectories that are too short that could be generated '''

path_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
path_directory = os.path.join(path_directory, "Dataset")
path_directory = os.path.join(path_directory, "Processed_dataset", "splitted_trajectories")

for path_it in os.listdir(path_directory):

    path = os.path.join(path_directory, path_it)

    for file in os.listdir(path):
        print("file", file)
        print("\n")
        csv_path = os.path.join(path, file)

        if csv_path.endswith('.csv'):
            try:
                # Calculate total distance
                total_distance = calc_distance(csv_path)
                print(total_distance)

                if total_distance > MAX_DISTANCE_PER_TRACK:
                    print(f'file {csv_path} remove because too long : {total_distance}')
                    os.remove(csv_path)
                
                if total_distance < MIN_DISTANCE_PER_TRACK:
                    print(f'file {csv_path} remove because too short : {total_distance}')
                    os.remove(csv_path)

            except Exception as e:
                # Print the traceback for debugging
                traceback.print_exc()
                # Delete the file if an error occurs
                if os.path.exists(csv_path):
                    os.remove(csv_path)
                    print(f"File {csv_path} deleted due to error: {e}")
