#!/bin/bash

PROCESSED_DIRECTORY="FALCON"
SPEED=10 #m/s
FILTER=120
HELICO=True
DILATATION_FACTOR=10.0
LENGTH_TRACK=5000
DILATATION_FACTOR_X=10.0
DILATATION_FACTOR_Y=5.0
DILATATION_FACTOR_Z=1.0

MAX_PER_SIMULATION=3 #20 #This parameters is for the maximum number of trajectories that could be played at the same times in a digital twin simulation

# Get the directory where the .csv files are 
script_dir="$PWD"
echo "Script directory: $script_dir"
script_dir=$(dirname "$script_dir")/Dataset/Processed_dataset/drones/trajectories_csv/$PROCESSED_DIRECTORY
echo "Current working directory $script_dir"

# Ensure script_dir ends with a slash to indicate it's a directory
if [[ ! $script_dir =~ /$ ]]; then
    script_dir="$script_dir/"
fi

# Initialize an empty array to store the substrings
substrings=()
group_of_same_trajectories=()

# Iterate over each item in the directory
for file in "$script_dir"*; do
    # Check if the item is a file (assuming you want to process .csv files)
    if [ -f "$file" ]; then
        # Extract the substring from the filename
        substring=$(basename "$file" | sed -E 's/_(log_drone[0-9]+_pyb\.csv)$//')

        # Check if the substring is not already in the array before appending
        if ! [[ " ${substrings[@]} " =~ " ${substring} " ]]; then
            substrings+=("$substring")
            #echo "happening $substring"
        fi
    else
        echo "Skipping non-file item: $file"
    fi
done

# Print the array of substrings
#echo "Substrings: ${substrings[@]}"

# Let's create the group of drones from the same original trajectories
for substring in "${substrings[@]}"; do
    sub_group_of_same_trajectories=()
    for file in "$script_dir"*; do
        if [ -f "$file" ]; then
            subfile=$(basename "$file" | sed -E 's/_(log_drone[0-9]+_pyb\.csv)$//')
            if [[ "$subfile" == "$substring" ]]; then
                sub_group_of_same_trajectories+=("$file")
            fi
        fi
    done
    group_of_same_trajectories+=("$(printf "%s\n" "${sub_group_of_same_trajectories[@]}")")
    #echo "Group for $substring: ${sub_group_of_same_trajectories[@]}"
done



##################### Let's convert the data throught the use of the python file #####################

path_python_xml_converter="$PWD"
path_python_xml_converter=$(dirname "$path_python_xml_converter")
path_python_xml_converter="${path_python_xml_converter}/Tools/convert_drones_trajectories_into_xml.py"

# Get the number of files in the directory 

# Count the number of element in array group_of_same_trajectories (=> number of different original trajectories)
length_directory=${#group_of_same_trajectories[@]}
# echo "length_directory $length_directory"
number_of_trajectories_needed=$((length_directory / MAX_PER_SIMULATION + 1))
# echo "Number of trajectories needed: $number_of_trajectories_needed"
sub_array_length=$(( ${#group_of_same_trajectories[@]} / $number_of_trajectories_needed ))

# create the sub-arrays

# echo "for loop $(seq 0 $((number_of_trajectories_needed - 1)))"
# echo "sub_array_length $sub_array_length"
for i in $(seq 0 $((number_of_trajectories_needed - 1)))
do
    # Calcultate the start and the end indices of the sub-arrays
    start_index=$(( i * $MAX_PER_SIMULATION))
    end_index=$(( (i + 1) * $MAX_PER_SIMULATION  ))
    # echo "start_index : $start_index"
    # echo "end_index : $end_index"

    # Create the sub_array using array slicing
    sub_array=("${group_of_same_trajectories[@]:$start_index:$MAX_PER_SIMULATION}")
    # It seems that there are no problems even with the last sub_array who is shorter and not has the length of MAX_PER_SIMULATION

    # Following of the code incoming
    echo " "
    echo "Sub_array $i : ${sub_array[@]}"
    echo " "

    # until now the code as no problem

    # Define the output path for the XML file
    output_path="$PWD"
    output_path=$(dirname "$output_path")
    output_path="${output_path}/Dataset/Processed_dataset/drones/trajectories_xml/$PROCESSED_DIRECTORY"

    tracks_number=$i

    # Check if the directory exists
    # Check if the directory exists and create it if it doesn't
    if [ ! -d "$output_path" ]; then
        mkdir -p "$output_path"
        echo "Directory created at: $output_path"
    fi
    output_path="${output_path}/trajscript${i}.xml"

    #echo "path_python_xml_converter : $path_python_xml_converter"

    # Construct the command to run the Python script
    cmd="python3 $path_python_xml_converter --list-path"

    # Add each file path as a separate argument to the command
    for path in "${sub_array[@]}"; do
        cmd+=" \"$path\""
    done
    # echo "############################################################"
    # echo "cmd with only the paths: $cmd"
    # echo "############################################################"

    # Add the remaining arguments to the command
    cmd+=" --output-path \"$output_path\" --speed \"$SPEED\" --filter \"$FILTER\" --helico \"$HELICO\" --length-track \"$LENGTH_TRACK\" --dilatation-factor \"$DILATATION_FACTOR\" --tracks-number \"$tracks_number\" --dilatation-factor-x \"$DILATATION_FACTOR_X\" --dilatation-factor-y \"$DILATATION_FACTOR_Y\" --dilatation-factor-z \"$DILATATION_FACTOR_Z\""

    # Output the final command for debugging purposes
    echo "Final command: $cmd"
    echo " "

    # Run the command
    eval "$cmd"

done
