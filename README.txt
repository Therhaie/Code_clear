0. (Alternative) Create the simulator environment
write all this command in the WSL consol when you are in the repository of "~/SimDrone6DOF-V1.0.0/src/drone_sim_6dof"
""" sudo apt install python3-venv """ 
""" python3 setup.py venv """ 
""" source .venv/bin/activate """ 
""" python3 -m pip install -r requirements.txt """ 
""" python3 setup.py build """ 
""" pip install pandas """
""" pip install datetime """
""" pip install basemap """
""" pip install tkinter """

command to update WSL to prevent error
""" sudo apt-get update """
""" sudo apt-get install jq """
""" sudo apt-get install bc """
""" sudo apt-get install python3-tk """


1. Create the simulator environment
- follow the readme instruction in the file "~/SimDrone6DOF-V1.0.0/src/drone_sim_6dof"
- """  python3 setup.py venv """"
- also add to the current virtual environment the Basemap Library if you what to be able to convert the raw data in the (lat/long/alt) into trajectories in the (x/y/z) format
- activate the virtual environment """ source .venv/bin/activate """
- build the project """ python3 setup.py build """
- also to the virtual environment the current library : panda, datetime, Basemap, (xml.etree.ElementTree)

2. Place the config file and waypoints file
- the config file in the """ SimDrone6DOF-V1.0.0\src\drone_sim_6dof\examples\config """
- the waypoints file in the """ C:\Users\ththy\Desktop\Stage_Thales\SimDrone6DOF-V1.0.0\src\drone_sim_6dof\examples\waypoints """
- you can also modify the conf.xml file to change the boids parameters and the drones parameters. (for indication of how to modify the value see the file observation_ENAC_software.txt )
- (run the script "Place_the_file") place the file "flock_personalized_conversion.json" in the directory "" SimDrone6DOF-V1.0.0\src\drone_sim_6dof\examples\config ""

3. Generate trajectories from the raw data

4. Split long trajectories into smaller one
in the directory script use the file " cutting_trajectories_into_smaller.py " to create the smaller trajectories, if you want to modify the lenght of the output track modify the value "" DISTANCE_PER_TRACK ""
(don't forget to clear the file in "Dataset/Processed_dataset/splitted_trajectories")

4.1 Convert the splitted trajectories into .JSON

4.2 Configure the simualtor
- create a file " processing " in the .JSON directory to implment the track that you want to process
- add the config file to the digital twin
- add the .xml


5. Launch simulation using the simulator from ENAC
- be sure that the file config.xml has the parameters that you want
( !!! If you modify the value some parameters in this file, before running the computation and starting converting the file. Take time to observe trajectories (= modify the parameters in the config.json file from "type": "csv" to "type": "play") in order to see if the simulation really do what you want)
	Things of which you should pay attention are :
	- if the drones are not to close 
	- if the drones follow the path wanted
	- if some stay in behind the flock doing turn around things (it's happend most of the time when there is a long curv, the last drone will just be left behind)
	- if the time of the simulation is good, that happends when you modify the value of "max_speed_kmh" and "max_speed" (= should not be too short otherwise you miss a portion of the trajectories, but the worst wase is when it's too long because when the drones will reached they end point they will start oscillation around the last position for the rest of the time of the simulation leading to an unusable simulation)
	 - 
- Select the number of drones that you want 
- put the json file that you want to handle in the directory " processing "
(I choose to proced this way because sometimes the computation can be very long and I want to be able to shutdown my computer between simulation)
- write in the script where do they come from in order to know where it should be placed as output

- run the bash script 
- the 

[ perhaps usefull to add a parameters of the processing of the dataset to add a parameters if you want to do it with 100% interaction or the script run without your interaction
-> after the simulation you see the actual speed and have the choice to modify it accordingly ]

6. Converting drones trajectories into digital twin files
The script """ Convert_drones_trajectories_into_digital_twin_tracks """ was created in order to reduce the time of simulation needed on the digital twin by combining multiple track from different trajectories into the same digial twin simulation. 
Parameters for the conversion of the output files from the ENAC simulatord into digital twin trajectories
- list-path [list of string] : list of the path that you want to process (normaly automatically handle by the script)
- speed [int] : speed that you want the drones to have after the modification (notice that you can also 
- filter [int] : parameter that filter the number of point coming from the output file that will be happend to the end file
- helico [Boolean] : parameter that enable you to add the feature "helicoter" on the digital twin
- lenght-track [int] : parameter that enable to put more trajectories into the same digital twin simulation
- dilatation-factor [float] : parameter that enable to increase the between each drones by this factor
- output-path [String] : parameters that indicate where the generated trajectories should be placed
- tracks-number [int] : parameter that change the name of the output file (normally totally handle by the script)
(- offset [list of int] : parameters to modify the starting point of your trajectories)

!! do not hesitate to increase the filter parameter to reduce the length of the output file in order to be able to play it on the digital twin
