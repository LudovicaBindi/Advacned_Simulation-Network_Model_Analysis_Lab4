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
run_length = 4 * 60  # run each replication for half a day

num_replications = 5
# get the delay distributions and bridges' breaking probabilities information
weight_dict = pd.read_csv('../data/scenario-weights.csv', index_col='Scenario').to_dict('index')

scenario = "BCSscore"
network = create_network(source_csv='../data/cleaned_roads_' + scenario + '.csv')
traffic_dict = read_traffic_probabilities(source='../data/traffic_probabilities.txt')

break_prob_min_experiments = [0.01, 0.05, 0.1]
break_prob_slope_experiments = [5, 10]

for min_setup in break_prob_min_experiments:
    for slope_setup in break_prob_slope_experiments:

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
                                            traffic_dict=traffic_dict,
                                            break_prob_min=min_setup, break_prob_slope=slope_setup)

                # Check if the seed is set
                print("SEED " + str(sim_model._seed))
                print("THIS RUN IS REPLICATION NUMBER", repl, "OF SCENARIO NUMBER", scenario)
                # One run with given steps
                for i in range(run_length):
                    sim_model.step()
                    # print("STEP", i, "COMPLETED")

                print('--------------------------------------------------------------------------')
                print('-----------------------------', 'Run Completed!', '-----------------------------')
                print('------------------------', str(time.time() - start_time), 'seconds', '------------------------')
                print('--------------------------------------------------------------------------')

                # export the experimental output to a “scenarioX.csv” file
                travel_time_df = sim_model.get_travel_time()
                travel_time_df.to_csv('../experiment/scenario_' + str(scenario) + '_' +
                                      str(slope_setup) + str(min_setup) +
                                      '_replication_' + str(repl) + '_travel_time.csv')
                waiting_time_df = sim_model.get_waiting_time()
                waiting_time_df.to_csv('../experiment/scenario_' + str(scenario) + '_' +
                                       str(slope_setup) + str(min_setup) +
                                       '_replication_' + str(repl) + '_waiting_time.csv')
