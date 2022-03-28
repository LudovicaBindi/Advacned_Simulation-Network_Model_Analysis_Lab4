from model import BangladeshModel
from network_creation import create_network
import pandas as pd
import time
import warnings

warnings.filterwarnings("ignore")  # to ignore depreciation warnings

"""
    Run simulation in a simplified environment (no probabilities)
"""

# ---------------------------------------------------------------


run_length = 7200

# create the graph
network = create_network(source_csv='../data/demo-4.csv')

# to take note of how long a replication takes
start_time = time.time()

sim_model = BangladeshModel(seed=123, network=network, file_name='../data/demo-4.csv')


# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run with given steps
for i in range(run_length):
    sim_model.step()

print('--------------------------------------------------------------------------')
print('-----------------------------', 'Run Completed!', '-----------------------------')
print('------------------------', str(time.time() - start_time), 'seconds', '------------------------')
print('--------------------------------------------------------------------------')

# get the data for the travel time
travel_time_df = sim_model.get_travel_time()
scenario = '-1'
repl = '-1'
travel_time_df.to_csv('../experiment/scenario_' + str(scenario) + '_replication_' + str(repl) + '_travel_time.csv')

waiting_time_df = sim_model.get_waiting_time()
waiting_time_df.to_csv('../experiment/scenario_' + str(scenario) + '_replication_' + str(repl) + '_waiting_time.csv')