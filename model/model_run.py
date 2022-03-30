from model import BangladeshModel
from network_creation import create_network
import pandas as pd
import time
import warnings

warnings.filterwarnings("ignore")  # to ignore depreciation warnings

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 1 x 24 hours; 1 tick 1 minute
run_length = 0.5 * 24 * 60

num_replications = 10
# run time 1000 ticks
# run_length = 1000
# weight_dict = pd.read_csv('../data/scenario-weights.csv', index_col='Scenario').to_dict('index')

seed = 1234567
scenario = "BCSscore"

# create the graph
network = create_network(source_csv='../data/cleaned_roads_' + scenario + '.csv')

# to take note of how long a replication takes
start_time = time.time()

sim_model = BangladeshModel(seed=seed, network=network,
                            file_name='../data/cleaned_roads_' + scenario + '.csv')
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
