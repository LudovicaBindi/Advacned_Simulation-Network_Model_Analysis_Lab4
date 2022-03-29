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

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 5 * 24 * 60

run_length = 7200
num_replications = 10
# run time 1000 ticks
# run_length = 1000
prob_dict_all = pd.read_csv('../data/scenario-weights.csv', index_col='Scenario').to_dict('index')

seed = 1234567
scenario = 1 # "allbroken"
print(prob_dict_all)

# create the graph
network = create_network(source_csv='../data/cleaned_roads.csv')

# to take note of how long a replication takes
start_time = time.time()

sim_model = BangladeshModel(seed=seed, network=network,
                            prob_bridges=prob_dict_all[str(scenario)], file_name='../data/cleaned_roads.csv')
#sim_model = BangladeshModel(seed=seed, network=network, file_name='../data/cleaned_roads.csv')
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
