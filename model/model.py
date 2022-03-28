from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from components import Source, Sink, SourceSink, Bridge, Link, Intersection, DataContainer
import pandas as pd
from collections import defaultdict
import networkx as nx
from network_creation import get_roads_name


# ---------------------------------------------------------------
def set_lat_lon_bound(lat_min, lat_max, lon_min, lon_max, edge_ratio=0.02):
    """
    Set the HTML continuous space canvas bounding box (for visualization)
    give the min and max latitudes and Longitudes in Decimal Degrees (DD)

    Add white borders at edges (default 2%) of the bounding box
    """

    lat_edge = (lat_max - lat_min) * edge_ratio
    lon_edge = (lon_max - lon_min) * edge_ratio

    x_max = lon_max + lon_edge
    y_max = lat_min - lat_edge
    x_min = lon_min - lon_edge
    y_min = lat_max + lat_edge
    return y_min, y_max, x_min, x_max


# ---------------------------------------------------------------
class BangladeshModel(Model):
    """
    The main (top-level) simulation model

    One tick represents one minute; this can be changed
    but the distance calculation need to be adapted accordingly

    Class Attributes:
    -----------------
    step_time: int
        step_time = 1 # 1 step is 1 min

    path_ids_dict: defaultdict
        Key: (origin, destination)
        Value: the shortest path (Infra component IDs) from an origin to a destination

        Only straight paths in the Demo are added into the dict;
        when there is a more complex network layout, the paths need to be managed differently

    sources: list
        all sources in the network

    sinks: list
        all sinks in the network

    prob_bridges: dictionary
        breaking probabilities per condition category

    delay_dist: dictionary
        distribution type and details per bridge length category for delay

    """

    step_time = 1

    # file_name = '../data/demo-4.csv'
    # file_name = '../data/hope.csv'
    file_name = '../data/cleaned_roads.csv'
    threshold_random_route = 0.5
    threshold_straight_route = 0.9
    threshold_shortest_route = 0.95

    def __init__(self, seed=None, x_max=500, y_max=500, x_min=0, y_min=0, network=None,
                 prob_bridges=defaultdict(float), delay_dist=defaultdict(str), file_name=None):
        super().__init__(seed=seed)
        self.schedule = BaseScheduler(self)
        self.running = True
        self.path_ids_dict = defaultdict(lambda: pd.Series())
        self.space = None
        self.sources = []
        self.sinks = []
        if file_name is not None:
            self.file_name = file_name

        # save the graph of the road network
        self.network = network

        self.prob_bridges = prob_bridges
        self.delay_dist = delay_dist

        self.generate_model()

        # create DataContainer to collect data
        self.data_container = DataContainer()

        # to take track of the closest sink to a source
        self.shortest_short_path = {}

    def generate_model(self):
        """
        generate the simulation model according to the csv file component information

        Warning: the labels are the same as the csv column labels
        """

        df = pd.read_csv(self.file_name)
        self.df = df
        # a list of names of roads to be generated
        # roads = ['N1', 'N2']
        roads = get_roads_name()

        df_objects_all = []
        for road in roads:
            # Select all the objects on a particular road in the original order as in the cvs
            df_objects_on_road = df[df['road'] == road]

            if not df_objects_on_road.empty:
                df_objects_all.append(df_objects_on_road)

                """
                Set the path 
                1. get the serie of object IDs on a given road in the cvs in the original order
                2. add the (straight) path to the path_ids_dict
                3. put the path in reversed order and reindex
                4. add the path to the path_ids_dict so that the vehicles can drive backwards too
                """
                path_ids = df_objects_on_road['id']
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids

                path_ids = path_ids[::-1]
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids

        # put back to df with selected roads so that min and max and be easily calculated
        df = pd.concat(df_objects_all)
        y_min, y_max, x_min, x_max = set_lat_lon_bound(
            df['lat'].min(),
            df['lat'].max(),
            df['lon'].min(),
            df['lon'].max(),
            0.05
        )

        # ContinuousSpace from the Mesa package;
        # not to be confused with the SimpleContinuousModule visualization
        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)

        for df in df_objects_all:

            for _, row in df.iterrows():  # index, row in ...

                # create agents according to model_type
                model_type = row['model_type'].strip()
                agent = None

                name = row['name']
                if pd.isna(name):
                    name = ""
                else:
                    name = name.strip()

                if model_type == 'source':
                    agent = Source(row['id'], self, row['length'], name, row['road'])
                    self.sources.append(agent.unique_id)
                elif model_type == 'sink':
                    agent = Sink(row['id'], self, row['length'], name, row['road'])
                    self.sinks.append(agent.unique_id)
                elif model_type == 'sourcesink':
                    agent = SourceSink(row['id'], self, row['length'], name, row['road'])
                    self.sources.append(agent.unique_id)
                    self.sinks.append(agent.unique_id)

                elif model_type == 'bridge':
                    # We made some changes in this part of the code.
                    # As they are now relevant for bridges, we are passing the following parameters:
                    # (1) the breaking probability based on condition
                    # (2) delay distribution based on length
                    delay_dist_dict = self.get_dist_dict(row['length'])
                    agent = Bridge(row['id'], self, row['length'], name, row['road'], row['condition'],
                                   self.prob_bridges[row['condition']], delay_dist_dict)
                elif model_type == 'link':
                    agent = Link(row['id'], self, row['length'], name, row['road'])
                elif model_type == 'intersection':
                    if not row['id'] in self.schedule._agents:
                        agent = Intersection(row['id'], self, row['length'], name, row['road'])

                if agent:
                    self.schedule.add(agent)
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)

    def get_default_dic(self):
        return self.path_ids_dict

    def get_random_route(self, source):
        """
        pick up a random route given an origin
        """
        while True:
            # different source and sink
            sink = self.random.choice(self.sinks)
            if sink is not source:
                break
        if not (source, sink) in self.path_ids_dict:
            self.path_ids_dict[source, sink] = pd.Series(
                nx.shortest_path(self.network, source=source, target=sink, weight='weight', method="dijkstra"))
        return self.path_ids_dict[source, sink]

    def get_route(self, source):
        #choose a route based on a certain probability
        result = None
        chance = self.random.random()
        if chance < BangladeshModel.threshold_random_route:
            result = self.get_random_route(source)
            if result is None:
                print('ERROR')
        elif chance < BangladeshModel.threshold_straight_route:
            result = self.get_straight_route(source)
            if result is None:
                print('ERROR')
        elif chance < BangladeshModel.threshold_shortest_route:
            result = self.get_shortest_short_path(source)
        else:
            result = self.get_longest_path(source)

        return result

    def get_straight_route(self, source):
        """
        pick up a straight route given an origin
        """
        return self.path_ids_dict[source, None]

    def get_shortest_short_path(self, source, weight='weight'):
        """
        Returns the path to the closest sink. Being 'close' is determined according to the specified weight parameter that
        describes an attribute of the edges in the network this BangladeshModel has. E.g., in case weight='weight' it means
        that this function will use the 'weight' attribute of the edges that could be, for example, the length between two
        points in a road (so 'closest' in this case means that to reach the target it'll take the least amount of Km).
        @param source: an edge in this BangladeshModel's network
        @param weight: the attribute of the edges in this BangladeshModel's network to be used when computing the closest
            sink
        @return: the path to reach the closes sink
        """
        # check if the path to the closest sink was already computed
        if source in self.shortest_short_path:
            return self.path_ids_dict[source, self.shortest_short_path[source]]

        # get the lengths of all the possible short path from the sink
        length_dict_all = nx.shortest_path_length(self.network, source, weight=weight, method='dijkstra')

        # get the target point of the shortest paths we are actually intersting in, the sinks
        targets = self.sinks

        # get the length of the shortest paths to our target points
        length_dict = {}
        for target in targets:
            length_dict[target] = length_dict_all[target]

        # make sure that the source is not in this list of target points
        if source in length_dict:
            length_dict.pop(source)

        # find the closest target point
        closest_target = min(length_dict, key=length_dict.get)

        # return the path to the closest target point: compute and save it if it is not stored yet
        if not (source, closest_target) in self.path_ids_dict:
            self.path_ids_dict[source, closest_target] = pd.Series(
                nx.shortest_path(self.network, source=source, target=closest_target, weight=weight, method="dijkstra"))

        # take track of which sink is the closest sink to the source
        self.shortest_short_path[source] = closest_target

        return self.path_ids_dict[source, closest_target]

    def length_calc(self, x):
        """"
        this function calculates the total length of a given path
        """
        total_length = 0
        for i in x: #iterate over paths
            idx = self.df.index[(self.df['id']) == i].tolist() # save the index of the row containing the specific LRP
                                                               # in a list
            index = idx[0]   #take the first element of the list
            total_length = total_length + self.df['length'][index] #calculate the total length of the path
        return total_length

    def get_longest_path(self, source):
        """"
        this function returns the path to the farthest sink based on the total length of the paths. For every possible
        sink, given a certain source, it calculates the length of every possible path to the sink and chooses the path
        with the biggest length. From all these longest paths, it picks the longest so at to define the sink
        towards which the truck must move. The key (source, "longest") is used so that we don't overwrite paths that
        already exist in the dictionary, where we store them.
        """
        #check whether this path exists already in the dictionary and if not calculate it
        if not (source, 'longest') in self.path_ids_dict:
            list_sinks = self.sinks
            check = False

            for this_sink in list_sinks: #iterate through all sinks
                if this_sink != source and this_sink is not None:
                    if check == False: #enter here only for the first sink
                        max_path = max(nx.all_simple_paths(self.network, source=source, target=this_sink),
                                       key=lambda x: self.length_calc(x)) #for all possible paths to the sink calculate their
                                                                          #length and choose the one with the biggest length
                        max_total_len = self.length_calc(max_path)   #save the length of the chosen path
                        check = True

                    else: #enter here for all sinks apart from the first one
                        this_path = max(nx.all_simple_paths(self.network, source=source, target=this_sink),
                                        key=lambda x: self.length_calc(x)) #for all possible paths to the sink calculate their
                                                                          #length and choose the one with the biggest length
                        total_len = self.length_calc(this_path) #save the length of the chosen path
                        if total_len > max_total_len: #check if the chosen path of this sink has bigger length than
                                                      # he chosen path of the previous sink
                            max_path = this_path     #save the path
                            max_total_len = total_len #save the path's length

            self.path_ids_dict[(source, 'longest')] = max_path #save the path to the dictionary

        return self.path_ids_dict[(source, 'longest')]

    # output = nx.all_simple_paths(net, source=1000000, target=1000027)
    # for path in output:
    #   print(path)
    # https://stackoverflow.com/questions/56657088/does-networkx-has-a-function-to-calculate-the-length-of-the-path-considering-wei

    def get_dist_dict(self, length):
        """
        Return the probability distribution dictionary of delay based on length
        """
        if length > 200:
            dict_to_return = self.delay_dist["over200"]
        elif length > 50:
            dict_to_return = self.delay_dist["from50to200"]
        elif length > 10:
            dict_to_return = self.delay_dist["from10to50"]
        else:
            dict_to_return = self.delay_dist["under10"]
        return dict_to_return

    def step(self):
        """
        Advance the simulation by one step.
        """
        self.schedule.step()

    def get_travel_time(self):
        """
        Returns the collected information about the travel time of the vehicles generated in the model and their total waiting time, along
        with the source that created the specified vehicle and the sink that removed it and he vehicle's type
        @return: a Pandas.DataFrame containing the information about vehicles travel time and their total waiting time
        """
        return self.data_container.get_travel_time()

    def get_waiting_time(self):
        """
        Returns the collected information about the waiting time of the vehicles generated in the model and their type
        @return: a Pandas.DataFrame containing the information about vehicles waiting time
        """
        return self.data_container.get_waiting_time()

# EOF -----------------------------------------------------------
