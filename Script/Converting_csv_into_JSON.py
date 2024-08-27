import json
import numpy as np
import pandas as pd
import os

def convert_into_json(path, destination_file_path):
    """
    Converts a CSV file into a JSON file at the specified destination path.
    """
    df = pd.read_csv(path)
    # Check if there are any NaN values in the DataFrame
    if df.isnull().values.any():
        print(f"Modifying file: {path}")
        # Fill NaN values with the last valid value
        df.fillna(method='ffill', inplace=True)
    else:
        print(f"No modifications needed for file (=no Nan value): {path}")
    list_of_lists = [[row['x'], row['y'], row['z']] for _, row in df.iterrows()]
    # Ensure the directory structure exists
    os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
    # Open the file in write mode, creating it if it doesn't exist
    with open(destination_file_path, 'w') as file:
        json.dump(list_of_lists, file, indent=2)

def main():
    """
    Main function to process CSV files and convert them into JSON format.
    """
    # Define the path to the directory containing the CSV files

    trajectories_path = os.path.dirname(__file__)
    trajectories_path = os.path.dirname(trajectories_path)
    directory_path = os.path.join(trajectories_path, "Dataset", "Processed_dataset", "splitted_trajectories" )


    #directory_path = rf'C:\Users\ththy\Desktop\Stage_Thales\birds_simulation_V_shape\Dataset\KITE'
    
    # Get every input directory
    # directories = [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]
    directories = [name for name in os.listdir(directory_path)]
    
    for directory in directories:
        # Define the output directory path
        output_path = os.path.dirname(__file__)
        output_path = os.path.dirname(output_path)
        output_path = os.path.join(output_path, "Dataset", "Processed_dataset", "drones", "trajectories_json_format", directory)
        print("output path", output_path)
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f'Directory created: {output_path}')
        
  
        # Find all .csv files in the Data_processed directory
        path_files = os.path.join(directory_path, directory)

        files = [ f for f in os.listdir(path_files) if f.endswith('.csv') ]

        for file in files:

            # Construct the destination path for the .json file
            base_name = os.path.splitext(file)[-2]
            print('base name', base_name)
            destination_file_path = os.path.join(output_path, base_name + '.json')
            
            print(f'\nProcessing file: {file} -> {destination_file_path}\n')
            path_input = os.path.join(path_files, file)
            print("\n")
            # print("File :", file)
            convert_into_json(path_input, destination_file_path)

if __name__ == "__main__":
    main()

