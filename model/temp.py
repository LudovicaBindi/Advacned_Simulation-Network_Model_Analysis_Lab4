from model import BangladeshModel
from network_creation import create_network
from components import Vehicle, SmallTruck
import pandas as pd
import time
import warnings

warnings.filterwarnings("ignore")  # to ignore depreciation warnings

"""
    Run simulation in a simplified environment (no probabilities)
"""

# ---------------------------------------------------------------
# create the graph
network = create_network(source_csv='../data/demo-4.csv')

# to take note of how long a replication takes
start_time = time.time()

sim_model = BangladeshModel(seed=123, network=network, file_name='../data/demo-4.csv')
c = Vehicle(1, sim_model, None)
print(c.speed)