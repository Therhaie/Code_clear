import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import traceback

''' This program aims to cut the long trajectories into smaller ones, in order to create a less heterogeneous dataset '''

# Get the path to the Tools directory
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
path = os.path.join(path, "Tools")
print(path)

# Add the path to the directory containing distance.py
sys.path.append(os.path.abspath(path))

# Import the distance function
from calc_distance_from_csv import calc_distance

DISTANCE_PER_TRACK = 5000  # distance wanted for the output tracks

path_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
path_directory = os.path.join(path_directory, "Dataset")
path_directory = os.path.join(path_directory, "Raw_trajectories")

# Use os.getcwd() to get the current working directory
current_working_dir = os.getcwd()

for path_it in os.listdir(path_directory):
    print("path it", path_it)
    path = os.path.join(path_directory, path_it)
    path = os.path.join(path, "Data_processed")
    
    for file in os.listdir(path):
        print("file", file)
        csv_path = os.path.join(path, file)
        
        if csv_path.endswith('.csv'):
            try:
                # Calculate total distance
                total_distance = calc_distance(csv_path)
                print(total_distance)

                if total_distance > DISTANCE_PER_TRACK:
                    name_i = 0
                    df = pd.read_csv(csv_path)
                    distance = 0
                    begin_term = 0

                    for id in range(df['x'].shape[0] - 1):
                        distance += ((df["x"].iloc[id+1] - df["x"].iloc[id])**2 + 
                                     (df["y"].iloc[id+1] - df["y"].iloc[id])**2 + 
                                     (df["z"].iloc[id+1] - df["z"].iloc[id])**2)**(1/2)

                        if distance > DISTANCE_PER_TRACK:
                            end_term = id
                            time = df['time'].iloc[begin_term:end_term]
                            x = df['x'].iloc[begin_term:end_term]
                            y = df['y'].iloc[begin_term:end_term]
                            z = df['z'].iloc[begin_term:end_term]

                            new_df = pd.DataFrame({'time': time, 'x': x, 'y': y, 'z': z})

                            parent_directory = os.path.dirname(csv_path)
                            parent_directory = os.path.dirname(parent_directory)
                            parent_directory = os.path.dirname(parent_directory)
                            parent_directory = os.path.dirname(parent_directory)
                            print("parent directory", parent_directory)

                            filename_with_ext = os.path.basename(csv_path)
                            filename_without_ext, _ = os.path.splitext(filename_with_ext)
                            new_filename = f"_sliced_{name_i}.csv"
                            new_path = os.path.join(parent_directory, "Processed_dataset", "splitted_trajectories", path_it, f"{filename_without_ext}_{new_filename}")

                            output_directory = os.path.dirname(new_path)
                            if not os.path.exists(output_directory):
                                os.makedirs(output_directory)
                            new_df.to_csv(new_path, index=False)

                            print("distance of the new generated trajectories calculated", calc_distance(new_path))
                            print("value of distance :", distance)
                            print("begin term :", begin_term)
                            print("end term :", end_term)
                            print("\n")

                            distance = 0
                            begin_term = id
                            name_i += 1

            except Exception as e:
                # Print the traceback for debugging
                traceback.print_exc()
                # Delete the file if an error occurs
                if os.path.exists(csv_path):
                    os.remove(csv_path)
                    print(f"File {csv_path} deleted due to error: {e}")



############################################### OLD CODE WITHOUT ERROR HANDLING ###########################################
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# # import tkinter as tk
# import sys


# ''' This programms aims to cut the long trajectories into smaller one, in order to create a less heteregenous dataset '''


# # Get the path to the Tools directory
# path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# # the path that his recieved by the function is either "/mnt/c/" or "C:\Users" depending of if you use windows or WSL
# path = os.path.join(path, "Tools")
# print(path)

# # Add the path to the directory containing distance.py
# sys.path.append(os.path.abspath(path))

# # import of distance function
# from calc_distance_from_csv import calc_distance

# DISTANCE_PER_TRACK = 5000 # distance wanted for the output tracks

# # def cut_trajectories_into_smaller(df, distance_per_track):

# path_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# path_directory = os.path.join(path_directory, "Dataset")
# path_directory = os.path.join(path_directory, "Raw_trajectories")

# # Use os.getcwd() to get the current working directory
# current_working_dir = os.getcwd()

# for path_it in os.listdir(path_directory):
#     print("path it", path_it)
#     # Construct the full path using the current working directory
#     print(path_it)
#     path = os.path.join(path_directory, path_it)
#     path = os.path.join(path, "Data_processed")
    
#     # now handle the case of the *.csv file

#     for file in os.listdir(path):
    
#         print("file", file)
#         # Correctly construct the path to the CSV file
#         csv_path = os.path.join(path, file)
#         if csv_path.endswith('.csv'):
#             # Now correctly read the CSV file

#             total_distance = calc_distance(csv_path)
#             print(total_distance)
#             if total_distance > DISTANCE_PER_TRACK:
#                 # Perhaps add a variation in the possible value in % of the value of the length of the track wanted
#                 name_i=0
#                 df = pd.read_csv(csv_path)
#                 distance=0
#                 begin_term=0
#                 #print("shape of the dataframe", df['x'].shape[0])
#                 for id in range(df['x'].shape[0]-1):
#                     # Get the distance current distance of the track generated
#                     distance+= ((df["x"].iloc[id+1]-df["x"].iloc[id])**2 + (df["y"].iloc[id+1]-df["y"].iloc[id])**2 + (df["z"].iloc[id+1]-df["z"].iloc[id])**2)**(1/2)
#                     # distance += ((df["x"].iloc[id+1] - df["x"].iloc[id])**2 + (df["y"].iloc[id+1] - df["y"].iloc[id])**2 +(df["z"].iloc[id+1] - df["z"].iloc[id])**2)**(1/2)
#                     if distance > DISTANCE_PER_TRACK:
#                         end_term=id
#                         time = df['time'].iloc[begin_term:end_term]
#                         x = df['x'].iloc[begin_term:end_term]
#                         y = df['y'].iloc[begin_term:end_term]
#                         z = df['z'].iloc[begin_term:end_term]

#                         new_df = pd.DataFrame({'time': time, 'x':x, 'y':y, 'z':z})

#                         parent_directory = os.path.dirname(csv_path)
#                         parent_directory = os.path.dirname(parent_directory)
#                         parent_directory = os.path.dirname(parent_directory)
#                         parent_directory = os.path.dirname(parent_directory)
#                         print("parent directory",parent_directory)

#                         # Remove the .csv extension from csv_path
#                         # Assuming csv_path is the full path to your CSV file
#                         filename_with_ext = os.path.basename(csv_path)
#                         filename_without_ext, _ = os.path.splitext(filename_with_ext)

#                         # Construct the new path in the parent directory
#                         new_filename = f"_sliced_{name_i}.csv"
#                         new_path = os.path.join(parent_directory, "Processed_dataset", "splitted_trajectories", path_it, f"{filename_without_ext}_{new_filename}")
#                         #print("final path", new_path)

#                         # Ensure the directory exists
#                         output_directory = os.path.dirname(new_path)
#                         if not os.path.exists(output_directory):
#                             os.makedirs(output_directory)
#                         new_df.to_csv(new_path, index=False)

#                         print("distance of the new generated trajectories calculated", calc_distance(new_path))
#                         print("value of distance :", distance)
#                         print("begin term :", begin_term)
#                         print("end term :", end_term)
#                         print("\n")


#                         # Update of the value
#                         distance=0
#                         begin_term=id
#                         name_i+=1


# ###################### old code which works ###################
# # '''This programms aims to cut the long trajectories into smaller one, in order to create a less heteregenous dataset '''


# # # Get the path to the Tools directory
# # path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# # # the path that his recieved by the function is either "/mnt/c/" or "C:\Users" depending of if you use windows or WSL
# # path = os.path.join(path, "Tools")
# # # print(path)

# # # Add the path to the directory containing distance.py
# # sys.path.append(os.path.abspath(path))

# # # import of distance function
# # from calc_distance_from_csv import calc_distance

# # DISTANCE_PER_TRACK = 5000 # distance wanted for the output tracks

# # # def cut_trajectories_into_smaller(df, distance_per_track):

# # path_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# # path_directory = os.path.join(path_directory, "Dataset")
# # path_directory = os.path.join(path_directory, "Raw_trajectories")

# # # Use os.getcwd() to get the current working directory
# # current_working_dir = os.getcwd()

# # for path_it in os.listdir(path_directory):
# #     print("path it", path_it)
# #     # Construct the full path using the current working directory
# #     print(path_it)
# #     path = os.path.join(path_directory, path_it)
# #     path = os.path.join(path, "Data_processed")
    
# #     # now handle the case of the *.csv file

# #     for file in os.listdir(path):
    
# #         print("file", file)
# #         # Correctly construct the path to the CSV file
# #         csv_path = os.path.join(path, file)
# #         if csv_path.endswith('.csv'):
# #             # Now correctly read the CSV file
# #             df = pd.read_csv(csv_path)
# #             total_distance = calc_distance(csv_path)
# #             print(total_distance)
# #             if total_distance > DISTANCE_PER_TRACK:
# #                 # Rewrite this part of the code to be sure that the generated tracks are really around 5000 m 
# #                 # Perhaps add a variation in the possible value in % of the value of the length of the track wanted
# #                 number_of_file = total_distance // DISTANCE_PER_TRACK
# #                 print(number_of_file)
# #                 length_of_a_track = df['x'].shape[0] // number_of_file
# #                 print("Number of point in the generated file",length_of_a_track)
# #                 # print(df['x'].shape)

# #                 # Cut the file into smaller one

# #                 for i in range(int(number_of_file)):
# #                     begin_term = int(i * length_of_a_track)  # Convert to integer
# #                     end_term = int((i + 1) * length_of_a_track)  # Convert to integer
# #                     time = df['time'].iloc[begin_term:end_term]  # Use iloc for integer-based indexing
# #                     x = df['x'].iloc[begin_term:end_term]  # Use iloc for integer-based indexing
# #                     y = df['y'].iloc[begin_term:end_term]  # Use iloc for integer-based indexing
# #                     z = df['z'].iloc[begin_term:end_term]  # Use iloc for integer-based indexing
                    
# #                     new_df = pd.DataFrame({'time': time, 'x':x, 'y':y, 'z':z})

# #                     parent_directory = os.path.dirname(csv_path)
# #                     parent_directory = os.path.dirname(parent_directory)
# #                     parent_directory = os.path.dirname(parent_directory)
# #                     parent_directory = os.path.dirname(parent_directory)
# #                     print("parent directory",parent_directory)

# #                     # Remove the .csv extension from csv_path
# #                     # Assuming csv_path is the full path to your CSV file
# #                     filename_with_ext = os.path.basename(csv_path)
# #                     filename_without_ext, _ = os.path.splitext(filename_with_ext)

# #                     # Construct the new path in the parent directory
# #                     new_filename = f"_sliced_{i}.csv"
# #                     new_path = os.path.join(parent_directory, "Processed_dataset", "splitted_trajectories", path_it, f"{filename_without_ext}_{new_filename}")
# #                     print("final path", new_path)

# #                     # Ensure the directory exists
# #                     output_directory = os.path.dirname(new_path)
# #                     if not os.path.exists(output_directory):
# #                         os.makedirs(output_directory)
# #                     new_df.to_csv(new_path, index=False)

# #                     print("distance of the new generated trajectories", calc_distance(new_path))
# #                     # print(output_directory)

# #                     # new_path = csv_path.replace('.csv', f'_sliced_{i}.csv')
# #                     # new_df.to_csv(new_path, index=False)
# #                     # print(new_path)


# #     # print(path)