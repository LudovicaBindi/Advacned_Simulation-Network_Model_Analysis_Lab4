from mesa.visualization.ModularVisualization import ModularServer
from ContinuousSpace.SimpleContinuousModule import SimpleCanvas
from model import BangladeshModel
from components import Source, Sink, Bridge, Link, Intersection, Infra, SourceSink
from network_creation import create_network
import pandas as pd
from components import read_traffic_probabilities

"""
Run simulation with Visualization 
Print output at terminal
"""


# ---------------------------------------------------------------
def agent_portrayal(agent):
    """
    Define the animation methode

    Only circles and rectangles are possible
    Both can be labelled
    """

    # define shapes
    portrayal = {
        "Shape": "circle",  # rect | circle
        "Filled": "true",
        "Color": "Khaki",
        "r": 2
        # "w": max(agent.population / 100000 * 4, 4),  # for "Shape": "rect"
        # "h": max(agent.population / 100000 * 4, 4)
    }

    if isinstance(agent, Source):
        if agent.vehicle_generated_flag:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "orange"

    elif isinstance(agent, Sink):
        if agent.vehicle_removed_toggle:
            portrayal["Color"] = "LightSkyBlue"
        else:
            portrayal["Color"] = "LightPink"

    elif isinstance(agent, Link):
        portrayal["Color"] = "Tan"

    elif isinstance(agent, Intersection):
        portrayal["Color"] = "DeepPink"

    elif isinstance(agent, Bridge):
        # highlight most critical bridges
        if agent.unique_id in top10_criticality:
            portrayal["Color"] = "purple"
        # highlight most vulnerable bridges
        elif agent.unique_id in top10_vulnerability:
            portrayal["Color"] = "blue"
        else:
            portrayal["Color"] = "gray"

    if isinstance(agent, (Source, Sink)):
        portrayal["r"] = 2
    elif isinstance(agent, Infra):
        portrayal["r"] = max(agent.vehicle_count * 4, 2)

    if agent.unique_id in top10_criticality or agent.unique_id in top10_vulnerability:
        portrayal["r"] = 5

    # define text labels
    # if isinstance(agent, Infra) and agent.name != "":
    #     if isinstance(agent, Source) or isinstance(agent, Sink) or isinstance(agent, SourceSink):
    #         portrayal["Text"] = agent.unique_id
    #     portrayal["Text_color"] = "DarkSlateGray"

    # define text labels
    # print only a label for the intersections
    if isinstance(agent, Intersection):
        # print only the names of the road the current Intersection conencts
        full_name = agent.unique_id
        left = full_name.split('-')[0]
        right = full_name.split('-')[1]
        left_road = left.split('_')[0]
        right_road = right.split('_')[0]
        portrayal["Text"] = left_road + '_' + right_road
    portrayal["Text_color"] = "DarkSlateGray"

    return portrayal


# ---------------------------------------------------------------
"""
Launch the animation server 
Open a browser tab 
"""

# get bridges data
top10_criticality = pd.read_csv('../data/top10_criticality.csv')['Bridge id'].tolist()
top10_vulnerability = pd.read_csv('../data/top10_vulnerability.csv')['Bridge id'].tolist()

# prepare data for the model
scenario = "BCSscore"
network = create_network(source_csv='../data/cleaned_roads_' + scenario + '.csv')
traffic_dict = read_traffic_probabilities(source='../data/traffic_probabilities.txt')

canvas_width = 400
canvas_height = 400

space = SimpleCanvas(agent_portrayal, canvas_width, canvas_height)
server = ModularServer(BangladeshModel,
                       [space],
                       "Transport Model Demo",
                       {"seed": 1234567, 'network': network, 'file_name': '../data/cleaned_roads_' + scenario + '.csv',
                        'traffic_dict': traffic_dict, 'break_prob_min': 0.01, 'break_prob_slope': 5})


# The default port
server.port = 8521
server.launch()
