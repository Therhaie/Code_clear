import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import os
from datetime import datetime, timedelta
import argparse

def init_funct():
    # Create an ElementTree object
    scenario = ET.Element('scenario')
    scenario.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    scenario.set('xsi:noNamespaceSchemaLocation', '.\scenario_V2.xsd')

    coordinates_center_position = ET.SubElement(scenario, 'coordinates_center_position')
    longitude = ET.SubElement(coordinates_center_position, 'longitude')
    longitude.text = '4.999999999999999'
    latitude = ET.SubElement(coordinates_center_position, 'latitude')
    latitude.text = '43.00000000000001'
    altitude = ET.SubElement(coordinates_center_position, 'altitude')
    altitude.text = '64.99999999906868'

    environment_parameters = ET.SubElement(scenario, 'environment_parameters')
    refraction_correction = ET.SubElement(environment_parameters, 'refraction_correction')
    refraction_correction.text = '0.25'

    entity_object = ET.SubElement(scenario, 'entity_object')
    entity_object.set('xsi:type', 'AirTarget')
    description = ET.SubElement(entity_object, 'description')
    description.text = 'This is the stationary Radar'
    start_time = ET.SubElement(entity_object, 'start_time')
    start_time.set('unit', 's')
    start_time.text = '0.0'

    characteristics = ET.SubElement(entity_object, 'characteristics')
    rcs = ET.SubElement(characteristics, 'rcs')
    rcs.set('unit', 'm2')
    rcs.text = '0.0'
    rcs_fluctuation = ET.SubElement(characteristics, 'rcs_fluctuation')
    rcs_fluctuation.text = 'NONE'

    trajectory = ET.SubElement(entity_object, 'trajectory')
    trajectory.set('xsi:type', 'BMTrajectory')
    initial_conditions = ET.SubElement(trajectory, 'initial_conditions')
    x = ET.SubElement(initial_conditions, 'x')
    x.set('unit', 'm')
    x.text = '0.0'
    y = ET.SubElement(initial_conditions, 'y')
    y.set('unit', 'm')
    y.text = '0.0'
    altitude = ET.SubElement(initial_conditions, 'altitude')
    altitude.set('unit', 'm')
    altitude.text = '65.0'
    vx = ET.SubElement(initial_conditions, 'vx')
    vx.set('unit', 'm/s')
    vx.text = '0.0'
    vy = ET.SubElement(initial_conditions, 'vy')
    vy.set('unit', 'm/s')
    vy.text = '0.0'

    bm_segments = ET.SubElement(trajectory, 'bm_segments')
    bm_segment = ET.SubElement(bm_segments, 'bm_segment')
    bm_segment.set('xsi:type', 'WaitSegment')
    duration = ET.SubElement(bm_segment, 'duration')
    duration.set('unit', 's')
    duration.text = '1500.0'

    return scenario

def adapt_speed_birds(data, speed_wanted=25):
    df = data
    dx = df['x'].iloc[-1] - df['x'].iloc[0]
    dy = df['y'].iloc[-1] - df['y'].iloc[0]
    dz = df['z'].iloc[-1] - df['z'].iloc[0]
    distance = (dx**2 + dy**2 + dz**2)**0.5
    print("distance:", distance)
    
    # Convert the start and end time to seconds
    start_time = df['time'].iloc[0].total_seconds()
    end_time = df['time'].iloc[-1].total_seconds()
    
    # Calculate the time duration in seconds
    time = end_time - start_time
    speed_current = distance / time
    f = speed_wanted / speed_current
    
    # Adjust the time column to adapt the speed
    df['time'] = df['time'] * 1 / f
    
    return df

def filter_trajectory(dataframe, step):
    filtered_dataframe = dataframe.iloc[::step]
    return filtered_dataframe 

def convert_to_datetime(dataframe):
    '''Convert the time column of the dataframe into a datetime object and subtract the first value from each element'''
    date_format = "%Y-%m-%d %H:%M:%S.%f"  # Ensure this matches the actual format in your dataset

    # Convert the 'time' column to datetime
    dataframe['time'] = pd.to_datetime(dataframe['time'], format=date_format)
    print('Original datetime values:', dataframe['time'])
    print('####################################################')

    # Subtract the first value from every element in the 'time' column
    first_time = dataframe['time'].iloc[0]  # Get the first time value as a datetime object
    dataframe['time'] = dataframe['time'] - first_time  # Subtract it from all other values

    print('Modified datetime values:', dataframe['time'])

    return dataframe

def add_offset(dataframe, offset):
    ''' Add an offset to every point in the dataframe given'''
    # print("before", dataframe['x'])
    dataframe['x'] += offset[0]
    dataframe['y'] += offset[1]
    dataframe['z'] += offset[2]
    # print("offset :", offset[0])
    # print("after", dataframe['x'])
    return dataframe

def end_function(scenario, directory, name_file):
    ''' Be sure that the path given do not contain any weird caracters like _ but just letters and numbers'''
    # Create a new file name
    print("\n")
    print("output path before handling", directory)
    print("\n")
    # split the string into two components, with the last component being the filename

    output_path = os.path.join(os.path.dirname(directory), name_file)
    # # Print the output path for debugging purposes
    print(f"Writing XML to: {output_path}")

    # Check if the directory exists
    # if not os.path.exists(directory):
    #     # If it doesn't exist, create it
    #     os.makedirs(directory)

    # Create an ElementTree object from the scenario
    tree = ET.ElementTree(scenario)

    # Write the XML to the output path
    tree.write(output_path, encoding="utf-8")

    # Print a success message
    print(f"XML written successfully to {output_path}")
    print("\n")

def write_csv(scenario, dataframe, speed=None, helico_parameter=False):
    ''' Same function as in the previous script so you need to create a new dataset to give to the function based on the initial dataset'''
    if speed is not None:
        dataframe = adapt_speed_birds(dataframe, speed)

    entity_object = ET.SubElement(scenario, 'entity_object')
    entity_object.set('xsi:type', 'AirTarget')
    description = ET.SubElement(entity_object, 'description')
    description.text = 'This is a drone'
    start_time = ET.SubElement(entity_object, 'start_time')
    start_time.set('unit', 's')
    start_time.text = '0.0'

    characteristics = ET.SubElement(entity_object, 'characteristics')
    target_type = ET.SubElement(characteristics, 'target_type')
    target_type.text = 'BOTH'
    target_kind = ET.SubElement(characteristics, 'target_kind')
    target_kind.text = 'AIRCRAFT'
    rcs = ET.SubElement(characteristics, 'rcs')
    rcs.set('unit', 'm2')
    rcs.text = '1.0'
    rcs_fluctuation = ET.SubElement(characteristics, 'rcs_fluctuation')
    rcs_fluctuation.text = 'NONE'

    if helico_parameter:
        helico = ET.SubElement(characteristics, 'helico')
        helico_kind = ET.SubElement(helico, 'helico_kind')
        helico_kind.text = 'HELICO_1'

    trajectory = ET.SubElement(entity_object, 'trajectory')
    trajectory.set('xsi:type', 'SampledTrajectory')

    for i in range(dataframe.shape[0]):
        samplePoint = ET.SubElement(trajectory, 'samplePoint')
        time = ET.SubElement(samplePoint, 'time')
        time.set('unit', 's')
        time.text = str(dataframe['time'].iloc[i].total_seconds())
        x = ET.SubElement(samplePoint, 'x')
        x.set('unit', 'm')
        x.text = str(dataframe['x'].iloc[i])
        y = ET.SubElement(samplePoint, 'y')
        y.set('unit', 'm')
        y.text = str(dataframe['y'].iloc[i])
        z = ET.SubElement(samplePoint, 'z')
        z.set('unit', 'm')
        z.text = str(dataframe['z'].iloc[i])

def parse_argument():
    parser = argparse.ArgumentParser(description='Convert a csv file into an xml file')
    parser.add_argument('--list-path', nargs='+', required=True, type=str, help='The path to the input csv file')
    parser.add_argument('--output_file', type=str, required=True, help='The path to the output xml file')
    parser.add_argument('--speed', type=int, default=25, required=True, help='The speed wanted for the birds')  
    #parser.add_argument('--step', type=int, default=1, required=True, help='The step to filter the data')
    parser.add_argument('--filter', type=int, default=10, help='Filter parameters that you want to implement')
    parser.add_argument('--helico', type=bool, help='If you want to actuvate the helico option')
    parser.add_argument('--tracks-number', type=int, required=True, help='This parameter is mandatory')
    parser.add_argument('--length-track', type=int, required=True, help='This parameters enable you to ')



    parser.add_argument('--offset', type=int, nargs=3, default=[0,0,0], help='The offset to add to the data')

    return parser.parse_args()

def main(list_path, speed, filter, helico_parameter, output_path, length_track, tracks_number):
    for id_group in range(len(list_path)):
        # pas de logique ici seulment de l'ecriture 

        for id_drones in range(len(list_path[id_group])):
            path = list_path[id_group][id_drones]
            
            write_csv(scenario, df, speed, helico_parameter)
    name_file = f"scenario_test{tracks_number}.xml"
    end_function(scenario, output_path, name_file)

if __name__ == "__main__":
    args = parse_argument()

    list_path = args.list_path
    output_path = args.output_file
    speed = args.speed
    # step = args.step
    tracks_number = args.tracks_number
    length_track = args.length_track
    filter = args.filter
    helico_parameter = args.helico

    print("list path", list_path)

    scenario = init_funct()
    # create the dataset that will be given to the function
    for track in list_path:
        print("track", track)
        print(" \n")
        # Get the number of birds in the dataset
        data = pd.read_csv(track)
        data = convert_to_datetime(data)
        num_birds = int((data.shape[1] - 1 ) / 3)
        # print("num birds", num_birds)
        # print("columns", data.columns)
        data.columns = data.columns.str.strip()
        for i in range(num_birds):
            print("key value of the dataset", data.keys()) 
            # print("data x", data[f'x_{i}'])
            # data_bird = pd.DataFrame({ 'time' : data['time'], 'x' : data[f'x_{i}'], 'y' : data[f'y_{i}'], 'z' : data[f'z_{i}']})
            data_bird = pd.DataFrame({ 'time' : data['time'], 'x' : data[f'x_0'], 'y' : data[f'y_0'], 'z' : data[f'z_0']})
            write_csv(scenario, data_bird, speed, helico_parameter)
    name_file = f"scenario_test{tracks_number}.xml"
    end_function(scenario, output_path, name_file)  





    # list_to_give=[]

    # # Generate the list_path that will be given as argument to the function
    # for group in list_path:
    #     group = group.split('\n')
    #     list_group=[]
    #     for trajectory in group:
    #         # print(trajectory)
    #         list_group.append(trajectory ) #+ '.csv')
    #     list_to_give.append(list_group)

    # main(list_to_give, speed, filter, dilatation_factor, helico, output_path, length_track, tracks_number)