from mesa.visualization.ModularVisualization import ModularServer
from ContinuousSpace.SimpleContinuousModule import SimpleCanvas
from model import BangladeshModel
from components import Source, Sink, Bridge, Link, Intersection, Infra, SourceSink
from network_creation import create_network

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
            portrayal["Color"] = "red"

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
        portrayal["Color"] = "dodgerblue"

    if isinstance(agent, (Source, Sink)):
        portrayal["r"] = 5
    elif isinstance(agent, Infra):
        portrayal["r"] = max(agent.vehicle_count * 4, 2)

    # define text labels
    if isinstance(agent, Infra) and agent.name != "":
        if isinstance(agent, Source) or isinstance(agent, Sink) or isinstance(agent, SourceSink):
            portrayal["Text"] = agent.unique_id
        portrayal["Text_color"] = "DarkSlateGray"

    return portrayal


# ---------------------------------------------------------------
"""
Launch the animation server 
Open a browser tab 
"""

canvas_width = 400
canvas_height = 400

space = SimpleCanvas(agent_portrayal, canvas_width, canvas_height)
network = create_network(source_csv='../data/cleaned_roads.csv')
server = ModularServer(BangladeshModel,
                       [space],
                       "Transport Model Demo",
                       {"seed": 1234567, 'network': network, 'file_name': '../data/cleaned_roads.csv'})

# The default port
server.port = 8521
server.launch()
