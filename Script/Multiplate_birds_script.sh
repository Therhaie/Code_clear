#!/bin/bash

NUMBER_OF_BIRDS_MIN=3
NUMBER_OF_BIRDS_MAX=14

DISTANCE_X=2
DISCTANCE_Y=1

# Get the directory where the .csv files are stored
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
csv_dir="$PWD"
csv_dir=$(dirname "$csv_dir")/Dataset/Processed_dataset/splitted_trajectories

for directory in $csv_dir/*; do
    if [ -d "$directory" ]; then
        echo "Processing directory $directory"

        # get the name of the directory
        directory_name=$(basename "$directory")
        echo "Directory name: $directory_name"

        for file in $directory/*; do

            # number birds per flock, generate this random number

            if [ -f "$file" ]; then

                # Extract the substring from the filename
                file_name=$(basename "$file")
                file_name="${file_name%.*}" # Remove the extension
                echo "File name: $file_name"

                # Generate the name of the output directory for the file
                output_directory="$PWD"
                output_directory=$(dirname "$output_directory")/Dataset/Processed_dataset/birds/trajectories_csv/$directory_name

                if [ ! -d "$output_directory" ]; then
                    mkdir -p "$output_directory"
                    echo "Directory created at: $output_directory"
                fi

                # Create the output file
                # python ....

                # Parameters for the python file

                flock_size=$((RANDOM % (NUMBER_OF_BIRDS_MAX - NUMBER_OF_BIRDS_MIN + 1) + NUMBER_OF_BIRDS_MIN))
                python_path=$(dirname "$PWD")/Tools/multiple_birds_generator.py
                input_trajectories=$file
                output_flock="${output_directory}/${file_name}_flock_$flock_size.csv"

                cmd="python3 $python_path --input_trajectories $input_trajectories --output_flock $output_flock --number_of_birds $flock_size --distance_x $DISTANCE_X --distance_y $DISCTANCE_Y"

                echo "Command: $cmd"
                eval "$cmd"

            fi
        done
    fi
done
