# Lab Assignment 4: Network Model Analysis v2

Created by: EPA1352 Group 3

|         Name         | Student Number |
|:--------------------:|:---------------|
|     Yaren Aslan      | 5257514        | 
|    Ludovica Bindi    | 5469856        |
|   Alexandre Curley   | 5500125        | 
| Aspasia Panagiotidou | 5631211        |
|   Dorukhan Yesilli   | 5539501        |


## Introduction

This project concerns a Simple Transport Model for Bangladesh. 
Currently, xxx roads are being simulated.
* More information about the model is available on [model/README.md](model/README.md) in the [model](model) directory.
* Input data and scenario settings can be explored on [data/README.md](data/README.md) in the [data](data) directory.
* Simulation outputs are available in the [experiment](experiment) directory. The output is explained in more detail on 
[experiment/README.md](experiment/README.md)
* Image and video outputs from the runs are presented in the [img](img) directory.


## How to Use

To run the simulation experiments and generate output data, run [model_run](model/model_run.py).

If you wish to visualize the simulation, run [model_viz](model/model_viz.py).

[model_video](model/model_video.py) saves a video recording of the simulation.

To take a closer look at the BangladeshModel and other structural components such as links and bridges as well as
the DataContainer, [model](model/model.py) and [component](model/components.py) scripts can be explored respectively.

Input data can be found in the [data](data) directory. User can inspect and change the 
[delay-distribution](data/delay-distribution.csv) and [scenario-settings](data/scenario-settings.csv) using csv files.

Currently, [roads](data/_roads3.csv) csv is being used when structural components are being created. 
It is possible to change the location of the file to be used on [model](model/model.py).

There are two notebooks included in the project. One is used to format the input data
([data_cleaning](model/data_cleaning.ipynb)), the other is used to visualize simulation outputs
([data_visualization](model/data_visualization.ipynb)).

## Files

```
EPA1352-G03-A3
│   README.md                       # this markdown document 
│
└───report
│   │   report.pdf                  # report of our analysis
│
└───notebook
│   │   centrality_metrics_analysis.ipynb # Betweenness centrality etc. analysis
│   │   cleaning_data.ipynb         # data cleaning file, uses BMMS_overview.xlsx & _roads3.csv
│   │   data_visualization.ipynb    # visualization file for output
│   │   Traffic data.ipynb          # Traffic data utilized to find generation probabilities for sim.
│   │   README.md                   # markdown for notebook folder
│   
└───model
│   └───ContinuousSpace             # directory containing files needed for visualization
│   │   components.py               # definition of classes of structural components and DataContainer
│   │   network_creation.py         # definition of the function which creates corresponding NetworkX model
│   │   model.py                    # definition of BangladeshModel class
│   │   model_run.py                # script to run the model for output generation
│   │   model_run_scenarios.py      # mainly used script to run the model for output generation based on scenarios
│   │   model_viz.py                # script to initiate visualization
│   │   model_viz_key_bridges_on_map.py   # script to initiate visualization including key bridges on map
│
└───img
│   │   N1.png                      # N1 with cleaned data
│   │   N1N2.png                    # N1, N2 and side roads with cleaned data
│   │   Critical and Vulnerable bridges.png     # Picture containing the critical and vulnerable bridges.
│   │   Critical and Vulnerable bridges - with legend.jpg  # Contains legend and the critical & vulnerable bridges.
│   │   distance_matrix example.png # an example png for the distance_matrix
│   
└───experiment
│   │   README.md                   # markdown for experiment folder
│   │   scenario_BCSscore_replication_0_travel_time.csv # Simulation Run Outputs
│   │   scenario_BCSscore_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_replication_0_travel_time.csv 
│   │   scenario_Cyclone_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Earthquake_replication_0_travel_time.csv 
│   │   scenario_Earthquake_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Flood_replication_0_travel_time.csv 
│   │   scenario_Flood_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_replication_0_travel_time.csv 
│   │   scenario_Erosion_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_10.1_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.1 
│   │   scenario_BCSscore_10.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_10.01_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.01 
│   │   scenario_BCSscore_10.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_10.05_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.05 
│   │   scenario_BCSscore_10.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_20.1_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.1 
│   │   scenario_BCSscore_20.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_20.01_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.01 
│   │   scenario_BCSscore_20.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_20.05_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.05 
│   │   scenario_BCSscore_20.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_50.1_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.1 
│   │   scenario_BCSscore_50.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_50.01_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.01 
│   │   scenario_BCSscore_50.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_50.05_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.05 
│   │   scenario_BCSscore_50.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_100.1_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.1 
│   │   scenario_BCSscore_100.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_100.01_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.01 
│   │   scenario_BCSscore_100.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_BCSscore_100.05_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.05 
│   │   scenario_BCSscore_100.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_10.1_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.1 
│   │   scenario_Cyclone_10.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_10.01_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.01 
│   │   scenario_Cyclone_10.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_10.05_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.05 
│   │   scenario_Cyclone_10.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_20.1_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.1 
│   │   scenario_Cyclone_20.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_20.01_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.01 
│   │   scenario_Cyclone_20.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_20.05_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.05 
│   │   scenario_Cyclone_20.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_50.1_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.1 
│   │   scenario_Cyclone_50.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_50.01_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.01 
│   │   scenario_Cyclone_50.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_50.05_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.05 
│   │   scenario_Cyclone_50.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_100.1_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.1 
│   │   scenario_Cyclone_100.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_100.01_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.01 
│   │   scenario_Cyclone_100.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Cyclone_100.05_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.05 
│   │   scenario_Cyclone_100.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_10.1_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.1 
│   │   scenario_Erosion_10.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_10.01_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.01 
│   │   scenario_Erosion_10.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_10.05_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.05 
│   │   scenario_Erosion_10.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_20.1_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.1 
│   │   scenario_Erosion_20.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_20.01_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.01 
│   │   scenario_Erosion_20.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_20.05_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.05 
│   │   scenario_Erosion_20.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_50.1_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.1 
│   │   scenario_Erosion_50.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_50.01_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.01 
│   │   scenario_Erosion_50.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_50.05_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.05 
│   │   scenario_Erosion_50.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_100.1_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.1 
│   │   scenario_Erosion_100.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_100.01_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.01 
│   │   scenario_Erosion_100.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_100.05_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.05 
│   │   scenario_Erosion_100.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_10.1_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.1 
│   │   scenario_Erosion_10.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_10.01_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.01 
│   │   scenario_Erosion_10.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_10.05_replication_0_travel_time.csv # Bridge breaking prob min 1, slope 0.05 
│   │   scenario_Erosion_10.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_20.1_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.1 
│   │   scenario_Erosion_20.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_20.01_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.01 
│   │   scenario_Erosion_20.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_20.05_replication_0_travel_time.csv # Bridge breaking prob min 2, slope 0.05 
│   │   scenario_Erosion_20.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_50.1_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.1 
│   │   scenario_Erosion_50.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_50.01_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.01 
│   │   scenario_Erosion_50.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_50.05_replication_0_travel_time.csv # Bridge breaking prob min 5, slope 0.05 
│   │   scenario_Erosion_50.05_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_100.1_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.1 
│   │   scenario_Erosion_100.1_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_100.01_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.01 
│   │   scenario_Erosion_100.01_replication_0_waiting_time.csv
│   │   ...
│   │   scenario_Erosion_100.05_replication_0_travel_time.csv # Bridge breaking prob min 10, slope 0.05 
│   │   scenario_Erosion_100.05_replication_0_waiting_time.csv
│   │   ...
│   
└───data
│   └───literary sources            # sources of literature
│   └───traffic files               # unpacked traffic files (.htm)
│   │   README.md                   # markdown for data folder
│   │   _roads3.csv                 # roads data
│   │   BMMS_overview.xlsx          # detailed bridge data
│   │   Bridges.xlsx                # detailed bridge data
│   │   bridges-scores.xlsx         # vulnerability scores of bridges
│   │   cleaned_roads.csv           # dataset created from cleaning_data.ipynb
│   │   cleaned_roads_BCSscore.csv  # dataset created from cleaning_data.ipynb
│   │   cleaned_roads_Cyclone.csv   # dataset created from cleaning_data.ipynb
│   │   cleaned_roads_Earthquake.csv # dataset created from cleaning_data.ipynb
│   │   cleaned_roads_Erosion.csv   # dataset created from cleaning_data.ipynb
│   │   cleaned_roads_Flood.csv     # dataset created from cleaning_data.ipynb
│   │   delay-distribution.csv      # based on bridge lengths
│   │   demo-4.csv                  # demo roads data, two straight roads
│   │   demo-4-original.csv         # original demo roads data, two straight roads
│   │   natural_hazards.xlsx        # vulnerability scores per natural hazard
│   │   RMMS.zip                    # original traffic data
│   │   roads_names.txt             # name of roads considered in the model
│   │   scenario-weights.csv        # scenario weights
│   │   top10_criticality.csv       # top 10 criticality road segments
│   │   top10_vulnerability.csv     # top 10 vulnerable road segments
│   │   traffic_probabilities.txt   # vehicle generation probabilities per road
│   │  

```