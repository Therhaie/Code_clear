#!/bin/bash

SPEED=10 #m/s
FILTER=120
HELICO=True
DILATATION_FACTOR=10.0
LENGTH_TRACK=5000

MAX_PER_SIMULATION=3 #20 #This parameters is for the maximum number of trajectories that could be played at the same times in a digital twin simulation

# get the directory where the .csv files are
script_dir="$PWD"
script_dir=$(dirname "$script_dir")/Dataset/Processed_dataset/birds/trajectories_csv

for directory in $script_dir/*; do
    if [ -d "$directory" ]; then
        echo "Processing directory $directory"

        # Get the name of the directory
        directory_name=$(basename "$directory")
        echo "Directory name: $directory_name"

        # Get the number of files in the directory to compute the number of files to create
        num_files=$(find "$directory" -type f -name "*.csv" | wc -l)
        echo "Number of files: $num_files"

        number_of_trajectories_needed=$((num_files / MAX_PER_SIMULATION + 1))
        echo "number of traj needed $number_of_trajectories_needed"
        
        # sub_array_length=$(( ${#group_of_same_trajectories[@]} / $number_of_trajectories_needed ))
        
        # echo "Number of trajectories needed: $number_of_trajectories_needed"
        # echo "$(seq 0 $((number_of_trajectories_needed - 1)))"

        # Create a group with all trajectories inside in order to simplify the process of creating the sub-arrays
        group_of_same_trajectories=()
        for file in "$directory"/*; do
            if [ -f "$file" ]; then
                group_of_same_trajectories+=("$file")
            fi
        done

        for i in $(seq 0 $((number_of_trajectories_needed - 1)))
        do

            # Calcultate the start and the end indices of the sub-arrays
            start_index=$(( i * $MAX_PER_SIMULATION))
            end_index=$(( (i + 1) * $MAX_PER_SIMULATION  ))
            echo "start_index: $start_index"
            echo "end_index: $end_index"
            echo " "

            # Create the sub_array using array slicing
            sub_array=("${group_of_same_trajectories[@]:$start_index:$MAX_PER_SIMULATION}")

            echo " "
            echo "Sub_array $i : ${sub_array[@]}"
            echo " "

            # Define the output path for the XML file
            output_path="$PWD"
            output_path=$(dirname "$output_path")/Dataset/Processed_dataset/birds/trajectories_xml/$directory_name
            echo "Output path: $output_path"
            echo " "

            # Check if the directory exists and create it if it doesn't
            if [ ! -d "$output_path" ]; then
                mkdir -p "$output_path"
                echo "Directory created at: $output_path"
            fi

            output_path="${output_path}/${directory_name}_trajscript${i}.xml"

            tracks_number=$i

            path_python_xml_converter=$(dirname "$PWD")/Tools/convert_birds_trajectories_into_xml.py

                # Construct the command to run the Python script
            cmd="python3 $path_python_xml_converter --list-path"

            # Add each file path as a separate argument to the command
            for path in "${sub_array[@]}"; do
                cmd+=" \"$path\""
            done

            cmd+=" --output_file \"$output_path\" --speed \"$SPEED\" --filter \"$FILTER\" --helico \"$HELICO\" --length-track \"$LENGTH_TRACK\" --tracks-number \"$tracks_number\""


            # Output the final command for debugging purposes
            echo "Final command: $cmd"
            echo " "

            # Run the command
            eval "$cmd"
        done
    fi
done

