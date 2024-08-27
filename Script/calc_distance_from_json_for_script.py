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

#################################### version of the code to be able to use it in the script ######################################################

def main():
    parser = argparse.ArgumentParser(description='Calculate the total distance travelled between waypoints.')
    parser.add_argument('-w', '--waypoints', type=str, required=True, help='Path to the JSON file containing waypoints.')
    args = parser.parse_args()
    
    if not os.path.isfile(args.waypoints):
        print(f"Error: {args.waypoints} is not a valid file.")
        sys.exit(1)

    with open(args.waypoints, 'r') as file:
        try:
            data = json.load(file)
            #print(f"Waypoints loaded: {args.waypoints}")
        except json.JSONDecodeError as e:
            #print(f"Error decoding JSON: {e}")
            sys.exit(1)
        
    distance = calc_distane(data)
    print(distance)
    return distance

if __name__ == '__main__':
    main()