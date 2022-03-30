from model import BangladeshModel
import pandas as pd
import random
from network_creation import create_network
from components import read_traffic_probabilities
import time
import warnings

warnings.filterwarnings("ignore")  # to ignore depreciation warnings

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 1 x 24 hours; 1 tick 1 minute
run_length =  12 * 60 # run each replication for half a day

num_replications = 10
# get the delay distributions and bridges' breaking probabilities information
weight_dict = pd.read_csv('../data/scenario-weights.csv', index_col='Scenario').to_dict('index')
weight_dict.pop("BCSscore")
weight_dict.pop("Cyclone")
weight_dict.pop("Flood")
# create the graph for the baseline (BCSscore) scenario
scenario = "BCSscore"
network = create_network(source_csv='../data/cleaned_roads_' + scenario + '.csv')
traffic_dict = read_traffic_probabilities(source='../data/traffic_probabilities.txt')

# run the simulation for each scenario
for scenario in weight_dict.keys():

    # run for num_replications times under each scenario setting
    for repl in range(num_replications):
        # get a seed
        seed = random.randint(0, 100000)

        # to take note of how long a replication takes
        start_time = time.time()
        # create the model
        sim_model = BangladeshModel(seed=seed, network=network,
                                    file_name='../data/cleaned_roads_' + scenario + '.csv',
                                    traffic_dict=traffic_dict)

        # Check if the seed is set
        print("SEED " + str(sim_model._seed))
        print("THIS RUN IS REPLICATION NUMBER", repl, "OF SCENARIO NUMBER", scenario)
        # One run with given steps
        for i in range(run_length):
            sim_model.step()
            #print("STEP", i, "COMPLETED")

        print('--------------------------------------------------------------------------')
        print('-----------------------------', 'Run Completed!', '-----------------------------')
        print('------------------------', str(time.time() - start_time), 'seconds', '------------------------')
        print('--------------------------------------------------------------------------')

        #export the experimental output to a “scenarioX.csv” file
        travel_time_df = sim_model.get_travel_time()
        travel_time_df.to_csv('../experiment/scenario_' + str(scenario) + '_replication_' + str(repl) + '_travel_time.csv')
        waiting_time_df = sim_model.get_waiting_time()
        waiting_time_df.to_csv('../experiment/scenario_' + str(scenario) + '_replication_' + str(repl) + '_waiting_time.csv')


"""
# to take note of how long a replication takes
start_time = time.time()
# run a 'baseline' scenario where the probability of bridges to break down is 0
scenario = 0
sim_model = BangladeshModel(seed=seed, network=network,
                            file_name='../data/cleaned_roads_' + scenario + '.csv')
# One run with given steps
for i in range(run_length):
    sim_model.step()

print('--------------------------------------------------------------------------')
print('-----------------------------', 'Run Completed!', '-----------------------------')
print('------------------------', str(time.time() - start_time), 'seconds', '------------------------')
print('--------------------------------------------------------------------------')

# export the experimental output to a “scenarioX.csv” file.
travel_time_df = sim_model.get_travel_time()
travel_time_df.to_csv('../experiment/scenario_0_replication_0_travel_time.csv')
waiting_time_df = sim_model.get_waiting_time()
waiting_time_df.to_csv('../experiment/scenario_0_replication_0_waiting_time.csv')
"""
