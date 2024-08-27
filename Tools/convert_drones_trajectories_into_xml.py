import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import os
from datetime import datetime, timedelta
import argparse

# todo : handle the fact that the output is in an other directory created because of the path problem
# can be fix by adding an other argument to parse, need to give the directory path + the name of the file OR can be fixe by turning the current received string into a string by it and then make a os.path.join with the different part of the string

# Todo : need to handle the fact that the inflatino between the drones still don't work
# 

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

def adapt_speed_drone(data, speed_wanted=25):
    df = data
    dx = df['x'].iloc[-1] - df['x'].iloc[0]
    dy = df['y'].iloc[-1] - df['y'].iloc[0]
    distance = (dx**2 + dy**2)**0.5
    print("distance", distance)
    start_time = int(df['time'].iloc[0])
    end_time = int(df['time'].iloc[-1])
    # start_time = pd.to_datetime(df['time'].iloc[0])
    # end_time = pd.to_datetime(df['time'].iloc[-1])
    # print("start", start_time)
    # print("end", end_time)
    time = end_time - start_time
    # print("time",time)
    speed_current = distance / int(time)
    # print("speed current", speed_current)
    f = speed_wanted / speed_current
    # print("valeur de f", f)
    # df['time'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()
    df['time'] = ((df['time']) * 1 / f)
    return df

def filter_trajectory(dataframe, step):
    filtered_dataframe = dataframe.iloc[::step]
    return filtered_dataframe 

def add_offset(dataframe, offset):
    ''' Add an offset to every point in the dataframe given'''
    # print("before", dataframe['x'])
    dataframe['x'] += offset[0]
    dataframe['y'] += offset[1]
    dataframe['z'] += offset[2]
    # print("offset :", offset[0])
    # print("after", dataframe['x'])
    return dataframe

def augment_distance(list_path, factor):
    '''This function aims to increase the distance between drone by multiplicating it
    the way of processing is for every drones, to calculate the neareast neighboor and then multiply it
    by a certain factor and then add it to
    output :  [[dx, dy, dz], ..., [dx, dy, dz]]'''

    id=0
    list_avg = []
    list_distance = []
    list_distance.append([0, 0, 0])
    for path in list_path:
        df = pd.read_csv(path)
        avg_position_x = df['x'].mean()
        avg_position_y = df['y'].mean()
        avg_position_z = df['z'].mean()
        # print("avg_position_x",avg_position_x)
        # print("avg_position_y",avg_position_y)
        # print("avg_position_z",avg_position_z)

        list_avg.append([avg_position_x, avg_position_y, avg_position_z])
    # print("list avg")
    # print(list_avg)
    for i in range(len(list_avg) - 1):
        d = [ list_avg[i+1][0] - list_avg[i][0], list_avg[i+1][1] - list_avg[i][1], list_avg[i+1][2] - list_avg[i][2] ]
        # print("value of d", d)
        list_distance.append(d)
        id += 1
    # print("list distance", list_distance)
    # print("dilatation factor", factor)
    print("list of the offset added to the drones", [ [ list_distance[k][0] * factor, list_distance[k][1] * factor, list_distance[k][2] * factor ] for k in range(len(list_distance)) ])

    return list_distance
    # return [ [ list_distance[k][0] * factor, list_distance[k][1] * factor, list_distance[k][2] * factor ] for k in range(id) ]

def write_csv(scenario, dataframe, speed=None, helico_parameter=False):
    if speed is not None:
        dataframe = adapt_speed_drone(dataframe, speed)

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
        time.text = str(dataframe['time'].iloc[i])
        x = ET.SubElement(samplePoint, 'x')
        x.set('unit', 'm')
        x.text = str(dataframe['x'].iloc[i])
        y = ET.SubElement(samplePoint, 'y')
        y.set('unit', 'm')
        y.text = str(dataframe['y'].iloc[i])
        z = ET.SubElement(samplePoint, 'z')
        z.set('unit', 'm')
        z.text = str(dataframe['z'].iloc[i])

def end_function(scenario, directory, name_file):
    ''' Be sure that the path given do not contain any weird caracters like _ but just letters and numbers'''
    # Create a new file name
    print("\n")
    print("output path before handling", directory)
    print("\n")
    # split the string into two components, with the last component being the filename

    # # print(type(directory))
    # print("#############################")
    # print("test with cast in path", os.path.dirname(directory))
    # print("#############################")
    # components = directory.rsplit("/", 1)


    # # #get the two components
    # path_c = components[0]
    # filename = components[1]  # No need to convert to str, it's already a string

    # # Ensure the filename ends with .xml
    # if not filename.endswith(".xml"):
    #     filename += ".xml"

    # # print the components
    # print("Path:", path_c)
    # print("Filename:", filename)
    # print("trajscript1.xml" == filename)
    # ##Create a new path by joining the directory and file name
    # output_path = os.path.join(path_c, f"{filename}")
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

def main(list_path, speed, filter, dilatation_factor, helico_parameter, output_path, length_track, tracks_number):
    scenario = init_funct()
    for id_group in range(len(list_path)):
        # print("\n")
        # print("group of drones currently handle : ", group)
        liste_increase_distance = augment_distance(list_path[id_group], dilatation_factor)
        print("\n")
        print(liste_increase_distance)
        print("\n")

        for id_drones in range(len(list_path[id_group])):
            path = list_path[id_group][id_drones]
            try:
                df = pd.read_csv(path)
                df = filter_trajectory(df, filter)
                # Proceed with operations on df here
            except Exception as e:
                print("---------------------------------------------------------------------------------")
                print("error when reading the file")
                print(f"Error reading file {path}: {str(e)}")
                print("---------------------------------------------------------------------------------")
            try:     
                # increase the distance between each drones
                # The error is here, lik with the fact that id is not an integer
                df = add_offset(df, liste_increase_distance[id_drones])
                df = add_offset(df, 30 * np.array([30,0,0]))

                # increase the distance between each trajectorie    s
                df = add_offset(df, np.array([5000 + 2 * length_track * id_group, 5000 + 2 * length_track, 0]))

            except:
                print("error in add offset")

            #df = add_offset(df, np.array([6000 * (id+1), 6000 , 0]))
            write_csv(scenario, df, speed, helico_parameter)
    name_file = f"scenario_test{tracks_number}.xml"
    end_function(scenario, output_path, name_file)

def parse_argument():
    '''
    Part of the code that handle the parsing of the argument'''
    parser = argparse.ArgumentParser(description="Processing csv file from the drones simulator into digital twin trajectories")
    parser.add_argument('--list-path', nargs='+', required=True, help='Path(s) of each file that you want to process')
    parser.add_argument('--speed', type=int, default=25, help='Speed of the drone in m/s that you want the drones to have')
    parser.add_argument('--filter', type=int, default=10, help='Filter parameters that you want to implement')
    parser.add_argument('--helico', type=bool, help='If you want to actuvate the helico option')
    parser.add_argument('--length-track', type=int, required=True, help='This parameters enable you to ')
    parser.add_argument('--dilatation-factor', type=float, default=2.0, required=True, help='This factor increase the distance between each drones in order to make the simulation more realistic')
    parser.add_argument('--output-path', type=str, required=True, help='This parameter is mandatory to know where the generated file goes')
    parser.add_argument('--tracks-number', type=int, required=True, help='This parameter is mandatory')

    # parser.add_argument('--offset', nargs='+', type=int, default=[0, 0, 0], help='Offset that you want to add to the drones')
    # parser.add_argument('--block-number'
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_argument()

    list_path = args.list_path
    speed = args.speed
    filter = args.filter
    helico = args.helico
    dilatation_factor = args.dilatation_factor
    output_path = args.output_path
    length_track = args.length_track # will be use later to setu the offset
    tracks_number = args.tracks_number

    list_to_give=[]

    # Generate the list_path that will be given as argument to the function
    for group in list_path:
        group = group.split('\n')
        list_group=[]
        for trajectory in group:
            # print(trajectory)
            list_group.append(trajectory ) #+ '.csv')
        list_to_give.append(list_group)

    main(list_to_give, speed, filter, dilatation_factor, helico, output_path, length_track, tracks_number)