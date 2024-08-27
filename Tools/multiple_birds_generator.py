import numpy as np 
import pandas as pd
import os
import argparse

''' The goal of this file is to take a trajectory as input and output a file with a flock of birds doing the same trajectory in a V-shape. '''

def multiply_birds(trajectory, number_of_birds, distance_x, distance_y, distance_z=0):
    '''
    Function that takes the input trajectory and multiply it by the number of birds.
    '''
    # Convert the list of list into a dataframe
    print("multiply_birds")
    #print(pd.read_csv(trajectory)['x'])
    trajectory_handle = pd.read_csv(trajectory)
    output_dataset = pd.read_csv(trajectory)
    # print("distance x ",type(distance_x))
    # print(trajectory_handle['x'])
    output_dataset = output_dataset.rename(columns={'x': 'x_0', 'y': 'y_0', 'z': 'z_0'})

    flock = []
    flock.append(trajectory_handle)
    for i in range(number_of_birds):
        # Create a new bird trajectory by modifying the original trajectory
        bird_x = trajectory_handle['x'] + (-1)**i * int(i * distance_x)
        bird_y = trajectory_handle['y'] + (i+2)//2 * distance_y
        bird_z = trajectory_handle['z'] #+ i * distance_z
        bird = np.array([bird_x, bird_y, bird_z]).T  # Transpose to align with the DataFrame structure
        output_dataset = pd.concat([output_dataset, pd.DataFrame({f'x_{i+1}': bird_x, f'y_{i+1}': bird_y, f'z_{i+1}': bird_z})], axis=1)
        # flock.append(pd.DataFrame(bird, columns=['x', 'y', 'z']))
        #print(f'Bird {i} done:\n{bird}')
    
    return output_dataset





def main(input_trajectories, output_flock, number_of_birds, distance_x, distance_y, distance_z) :
    '''
    Main function that takes the input trajectory and output the flock of birds doing the same trajectory in a V-shape.
    '''
    # Load the input trajectory
    print("main")
    #trajectory = pd.read_csv(input_trajectories)
    flock = multiply_birds(input_trajectories, number_of_birds, distance_x, distance_y, distance_z=0)

    # Convert the list of DataFrame into a single DataFrame
    print("flock", flock)
    flock.to_csv(output_flock, index=False)

def parse_argument():
    '''
    Part of the code that handle the parsing of the argument'''
    parser = argparse.ArgumentParser(description='Generate a flock of birds doing the same trajectory in a V-shape.')
    parser.add_argument('--input_trajectories', required=True, help='Path to the input trajectory file.')
    parser.add_argument('--output_flock', required=True, help='Path to the output flock file.')
    parser.add_argument('--number_of_birds', type=int, required=True, help='Number of birds in the flock.')
    parser.add_argument('--distance_x', type=float, required=True, help='Distance between the birds in the x-axis.')
    parser.add_argument('--distance_y', type=float, required=True, help='Distance between the birds in the y-axis.')
    parser.add_argument('--distance_z', type=float, help='Distance between the birds in the z-axis.')
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_argument()

    input_trajectories = args.input_trajectories
    output_flock = args.output_flock
    number_of_birds = args.number_of_birds -1 # We remove 1 because the original trajectory is already counted
    distance_x = args.distance_x
    distance_y = args.distance_y
    distance_z = args.distance_z
    print("Input trajectory: ")
    
    main(input_trajectories, output_flock, number_of_birds, distance_x, distance_y, distance_z) 


