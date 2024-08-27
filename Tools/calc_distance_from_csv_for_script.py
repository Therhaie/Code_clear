import json
import sys
import os
import argparse
from math import sqrt, isnan

def calc_distane(data):
    distance = 0
    for i in range(1, len(data)):
        distance += sqrt((data[i][0] - data[i-1][0])**2 + (data[i][1] - data[i-1][1])**2 + (data[i][2] - data[i-1][2])**2 )
    return distance

################################ code to handle .csv file #######################################

import argparse
import numpy as np
import pandas as pd

def calc_distance(path, verbose=False):
    """
    Calculates the total distance between consecutive points in a CSV file containing 'x' and 'y' columns.

    Args:
        path (str): Path to the CSV file.
        verbose (bool, optional): Whether to print detailed information during processing. Defaults to False.

    Returns:
        float: The total calculated distance.

    Raises:
        FileNotFoundError: If the specified file path is not found.
        ValueError: If the CSV file does not contain 'x' and 'y' columns.
    """

    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")

    if 'x' not in df.columns or 'y' not in df.columns:
        raise ValueError(f"CSV file '{path}' must contain 'x' and 'y' columns.")

    distance = 0
    for i in range(df['x'].shape[0] - 1):
        x_diff = df['x'].iloc[i + 1] - df['x'].iloc[i]
        y_diff = df['y'].iloc[i + 1] - df['y'].iloc[i]
        distance += np.sqrt(x_diff**2 + y_diff**2)

    if verbose:
        print(f"Total distance between points in '{path}': {distance}")

    return distance

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate total distance from a CSV file.')
    parser.add_argument(
        '-w', '--path_waypoints',
        type=str, required=True,
        help='Path to waypoint file')
    parser.add_argument('--verbose', action='store_true', default=False,
                        help='Print detailed information during processing.')

    args = parser.parse_args()

    try:
        total_distance = calc_distance(args.path_waypoints, verbose=args.verbose)
        print(total_distance)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        exit(1)