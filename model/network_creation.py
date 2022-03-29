import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def create_network(source_csv='../data/demo-4.csv'):
    """
    Creates a graph from the description contained in the specified source csv file
    @param source_csv: the csv file containing the description of the graph to be built
    @return: a NetworkX.Graph of the data containted in the specified source csv file
    """
    # assumptions: the LRPS and LRPE have a length of 0

    # read the data
    network_data = pd.read_csv(source_csv)
    # create empty graph
    network = nx.Graph()

    # get the roads' names we are analyzing
    # roads = ['N1', 'N2']
    roads = get_roads_name()

    # iterate through the roads
    for road in roads:
        # get the data for the road
        road_df = network_data.loc[network_data['road'] == road]

        first_element = False  # False if the first element hasn't been visited

        # iterate through the elements of this road
        for index, row in road_df.iterrows():
            # get the type value that will be saved in the node
            type = None
            if row['model_type'] == 'bridge': # if it is a bridge, then save the condition information in the type value
                type = row['model_type'] + '-' + str(row['break_prob'])
            else:
                type = row['model_type']

            # add the node
            network.add_node(row['id'], type=type)  # save the information about the model_type in the node

            # add the nedge that connects this element to the previous one
            if first_element == True:
                network.add_edge(row['id'], network_data.iloc[index - 1]['id'], weight=row['length'])
            else:
                first_element = True

    return network

def get_roads_name(source='../data/roads_names.txt'):
    """
    Gets the roads that must be analyzed in this model
    @param source: a txt file where the roads name are specified each on a new line
    @return: a list containing all the roads to be analyzed in this model
    """
    roads = []

    with open(source) as f:  # open the file
        for line in f:  # read all the lines in the file
            road = line.rstrip('\n')  # remove the trailing newline
            roads.append(road)  # append the road name

    return roads