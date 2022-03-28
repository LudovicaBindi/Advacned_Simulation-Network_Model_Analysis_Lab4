from mesa import Agent
from enum import Enum
from collections import defaultdict
import pandas as pd


# ---------------------------------------------------------------

class Infra(Agent):
    """
    Base class for all infrastructure components

    Attributes
    __________
    vehicle_count : int
        the number of vehicles that are currently in/on (or totally generated/removed by)
        this infrastructure component

    length : float
        the length in meters
    ...

    """

    def __init__(self, unique_id, model, length=0,
                 name='Unknown', road_name='Unknown'):
        super().__init__(unique_id, model)
        self.length = length
        self.name = name
        self.road_name = road_name
        self.vehicle_count = 0

    def step(self):
        pass

    def __str__(self):
        return type(self).__name__ + str(self.unique_id)


# ---------------------------------------------------------------
class Bridge(Infra):
    """
    Creates delay time

    Attributes
    __________
    condition:
        condition of the bridge

    delay_time: int
        the delay (in ticks) caused by this bridge

    break_prob: float
        probability of the bridge to break

    delay_dist: dictionary
        distribution type and details to create delay time
            delay_dist["type"]: triangular/uniform
            delay_dist["value-x"]: xth parameter required for the distribution

    """

    def __init__(self, unique_id, model, length=0,
                 name='Unknown', road_name='Unknown', condition='Unknown',
                 break_prob=0, delay_dist=defaultdict(str)):
        super().__init__(unique_id, model, length, name, road_name)

        self.condition = condition
        self.break_prob = break_prob
        self.status = self.get_status()  # whether the bridge is broken or not

        self.delay_time = 0
        self.delay_distribution = delay_dist  # self.random.randrange(0, 10)
        # print(self.delay_time)
        self.last_delay_time_given = 0

    def get_status(self):
        """
        determine the status of the bridge based on breaking probability
        @return: status ("broken" or "working")
        """
        if self.random.random() < self.break_prob:
        #if self.random.random() < 1:
            status = "broken"
        else:
            status = "working"
        print("Status for bridge", self.unique_id, "is set to", status)
        return status

    def get_delay_time(self):
        """
        creates delay time according to bridge status and delay_distribution
        """

        if self.status == "broken":
            if self.delay_distribution["type"] == "triangular":
                self.delay_time = self.random.triangular(self.delay_distribution["value-0"],
                                                         self.delay_distribution["value-1"],
                                                         self.delay_distribution["value-2"])

            elif self.delay_distribution["type"] == "uniform":
                self.delay_time = self.random.randrange(self.delay_distribution["value-0"],
                                                        self.delay_distribution["value-1"])

        return self.delay_time

        # self.delay_time = 5
        # return self.delay_time

    def get_delay_time_traffic_jam(self):
        """
        Returns a waiting time for this bridge according to a FIFO logic: if there are other vehicles already waiting at
        this bridge, then the last vehicle must wait that those vehicles go on the bridge first and then the vehicle can
        go as well
        @return: returns a waiting time for this bridge according to a FIFO logic
        """
        # if there are other vehicles waiting (it means that the bridge already assigned some delay time)
        if self.last_delay_time_given > 0:
            self.last_delay_time_given += 1 # add an extra delay because this last vehicle must wait for the other vehicles to live the bridge
        else:
            # if this vehicle is the first one to arrive, then we must get a delay time according to the conditions of the bridge
            self.last_delay_time_given = self.get_delay_time()

        return self.last_delay_time_given


# ---------------------------------------------------------------
class Link(Infra):
    pass


# ---------------------------------------------------------------
class Intersection(Infra):
    pass


# ---------------------------------------------------------------
class Sink(Infra):
    """
    Sink removes vehicles

    Attributes
    __________
    vehicle_removed_toggle: bool
        toggles each time when a vehicle is removed
    ...

    """
    vehicle_removed_toggle = False

    def remove(self, vehicle):
        self.model.schedule.remove(vehicle)
        self.vehicle_removed_toggle = not self.vehicle_removed_toggle
        print(str(self) + ' REMOVE ' + str(vehicle))


# ---------------------------------------------------------------

class Source(Infra):
    """
    Source generates vehicles

    Class Attributes:
    -----------------
    truck_counter : int
        the number of trucks generated by ALL sources. Used as Truck ID!

    Attributes
    __________
    generation_frequency: int
        the frequency (the number of ticks) by which a truck is generated

    vehicle_generated_flag: bool
        True when a Truck is generated in this tick; False otherwise
    ...

    """

    truck_counter = 0
    generation_frequency = 5
    vehicle_generated_flag = False
    # a series of threshold to create the different kinds of vehicles
    prob_large_bus = 0.2
    prob_truck = 0.5
    prob_small_truck = 0.75
    prob_mini_bus = 1

    def step(self):
        if self.model.schedule.steps % self.generation_frequency == 0:
            self.generate_vehicle()
        else:
            self.vehicle_generated_flag = False

    def create_a_vehicle(self):
        """
        Returns a Vehicle. The different vehicles are generated according to previously stated probabilities
        @return: returns a Vehicle
        """
        # "toss a coin"
        chance = self.random.random()

        # according to the random value, we create a Vehicle
        # the probabilities used here are increasing threshold
        if chance < self.prob_large_bus:
            result = LargeBus('LargeBus' + str(Source.truck_counter), self.model, self)
        elif chance < self.prob_truck:
            result = Truck('Truck' + str(Source.truck_counter), self.model, self)
        elif chance < self.prob_small_truck:
            result = SmallTruck('SmallTruck' + str(Source.truck_counter), self.model, self)
        else:
            # if chance <= self.prob_mini_bus
            result = MiniBus('MiniBus' + str(Source.truck_counter), self.model, self)

        return result

    def generate_vehicle(self):
        """
        Generates a truck, sets its path, increases the global and local counters
        """
        try:
            # agent = Vehicle('Truck' + str(Source.truck_counter), self.model, self)
            agent = self.create_a_vehicle()
            if agent:
                self.model.schedule.add(agent)
                agent.set_path()
                Source.truck_counter += 1
                self.vehicle_count += 1
                self.vehicle_generated_flag = True
                print(str(self) + " GENERATE " + str(agent))
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")


# ---------------------------------------------------------------
class SourceSink(Source, Sink):
    """
    Generates and removes trucks
    """
    pass


# ---------------------------------------------------------------
class Vehicle(Agent):
    """

    Attributes
    __________
    speed: float
        speed in meter per minute (m/min)

    step_time: int
        the number of minutes (or seconds) a tick represents
        Used as a base to change unites

    state: Enum (DRIVE | WAIT)
        state of the vehicle

    location: Infra
        reference to the Infra where the vehicle is located

    location_offset: float
        the location offset in meters relative to the starting point of
        the Infra, which has a certain length
        i.e. location_offset < length

    path_ids: Series
        the whole path (origin and destination) where the vehicle shall drive
        It consists the Infras' uniques IDs in a sequential order

    location_index: int
        a pointer to the current Infra in "path_ids" (above)
        i.e. the id of self.location is self.path_ids[self.location_index]

    waiting_time: int
        the time the vehicle needs to wait

    generated_at_step: int
        the timestamp (number of ticks) that the vehicle is generated

    removed_at_step: int
        the timestamp (number of ticks) that the vehicle is removed
    ...

    """

    # 48 km/h translated into meter per min
    speed = 48 * 1000 / 60
    # One tick represents 1 minute
    step_time = 1

    class State(Enum):
        DRIVE = 1
        WAIT = 2

    def __init__(self, unique_id, model, generated_by,
                 location_offset=0, path_ids=None):
        super().__init__(unique_id, model)
        self.generated_by = generated_by
        self.generated_at_step = model.schedule.steps
        self.location = generated_by
        self.location_offset = location_offset
        self.pos = generated_by.pos
        self.path_ids = path_ids
        # default values
        self.state = Vehicle.State.DRIVE
        self.location_index = 0
        self.waiting_time = 0
        self.waited_at = None
        self.removed_at_step = None
        self.accumulated_waiting_time = 0  # counter for the total waiting time

    def __str__(self):
        return "Vehicle" + str(self.unique_id) + \
               " +" + str(self.generated_at_step) + " -" + str(self.removed_at_step) + \
               " " + str(self.state) + '(' + str(self.waiting_time) + ') ' + \
               str(self.location) + '(' + str(self.location.vehicle_count) + ') ' + str(self.location_offset)

    def set_path(self):
        """
        Set the origin destination path of the vehicle
        """
        self.path_ids = self.model.get_route(self.generated_by.unique_id)
        # print(self.path_ids)

    def step(self):
        """
        Vehicle waits or drives at each step
        """
        if self.state == Vehicle.State.WAIT:
            self.waiting_time = max(self.waiting_time - 1, 0)
            if self.waiting_time == 0:
                self.waited_at = self.location
                self.state = Vehicle.State.DRIVE

        if self.state == Vehicle.State.DRIVE:
            self.drive()

        """
        To print the vehicle trajectory at each step
        """
        # print(self)

    def drive(self):

        # the distance that vehicle drives in a tick
        # speed is global now: can change to instance object when individual speed is needed
        distance = Vehicle.speed * Vehicle.step_time
        distance_rest = self.location_offset + distance - self.location.length

        if distance_rest > 0:
            # go to the next object
            self.drive_to_next(distance_rest)
        else:
            # remain on the same object
            self.location_offset += distance

    def drive_to_next(self, distance):
        """
        vehicle shall move to the next object with the given distance
        """

        self.location_index += 1

        next_id = self.path_ids[self.location_index]

        # print(self.unique_id)
        # print(distance)
        next_infra = self.model.schedule._agents[next_id]  # Access to protected member _agents
        # print(next_infra)

        if isinstance(next_infra, Sink):
            # arrive at the sink
            self.arrive_at_next(next_infra, 0)
            self.removed_at_step = self.model.schedule.steps
            self.location.remove(self)
            # make sure the model takes tracks of the travel time of this truck
            self.model.data_container.insert_travel_time(self.unique_id, self.removed_at_step - self.generated_at_step,
                                                         self.accumulated_waiting_time, self.generated_by.unique_id,
                                                         next_infra.unique_id, self.__class__.__name__)
            return
        elif isinstance(next_infra, Bridge):
            #self.waiting_time = next_infra.get_delay_time()
            self.waiting_time = next_infra.get_delay_time_traffic_jam()
            if self.waiting_time > 0:
                # arrive at the bridge and wait
                self.arrive_at_next(next_infra, 0)
                self.state = Vehicle.State.WAIT
                # make sure the model takes tracks of the waiting time of this truck
                self.model.data_container.insert_waiting_time(self.unique_id, next_infra.unique_id, self.waiting_time,
                                                              self.__class__.__name__)
                self.accumulated_waiting_time += self.waiting_time  # update waiting time counter
                return
            # else, continue driving
        # print('distance')
        # print(distance)
        # print('next infra length')
        # print(next_infra.length)

        if next_infra.length > distance:
            # stay on this object:
            self.arrive_at_next(next_infra, distance)
        else:
            # drive to next object:
            self.drive_to_next(distance - next_infra.length)

    def arrive_at_next(self, next_infra, location_offset):
        """
        Arrive at next_infra with the given location_offset
        """
        self.location.vehicle_count -= 1

        # if this is the last vehicle waiting on a bridge, then there is no queue anymore
        # so reset the variable that takes track of the last given waiting time
        if isinstance(self.location, Bridge) and self.location.vehicle_count == 0:
            self.location.last_delay_time_given = 0

        self.location = next_infra
        self.location_offset = location_offset
        self.location.vehicle_count += 1




class LargeBus(Vehicle):
    # 37 km/h translated into meter per min
    speed = 37 * 1000 / 60


class Truck(Vehicle):
    # 31 km/h translated into meter per min
    speed = 31 * 1000 / 60


class SmallTruck(Vehicle):
    # 29 km/h translated into meter per min
    speed = 29 * 1000 / 60


class MiniBus(Vehicle):
    # 26 km/h translated into meter per min
    speed = 26 * 1000 / 60


# ---------------------------------------------------------------
class DataContainer:
    """
    Class used to collect the data from the model

    Attributes
    __________
    travel_time_df: Pandas.DataFrame
        dataframe used to collect data for the average travel time of the trucks and the total waiting time

    waiting_time_df: Pandas.DataFrame
        dataframe used to collect data for the waiting time on bridges

    """

    def __init__(self):
        # dataframe to put the collected information in
        self.travel_time_df_columns = ['Truck id', 'Travel time', 'Total waiting time', 'Created at', 'Removed at',
                                       'Type']
        self.waiting_time_df_columns = ['Truck id', 'Bridge id', 'Waiting time', 'Type']
        self.travel_time_df = pd.DataFrame(columns=self.travel_time_df_columns)
        self.waiting_time_df = pd.DataFrame(columns=self.waiting_time_df_columns)

    def insert_travel_time(self, truck_id, travel_time, total_waiting_time=None, created_by=None, removed_at=None,
                           type=None):
        """
        Saves the specified travel time and the total waiting time of the given vehicle, along with the source that created the
        specified vehicle and the sink that removed it and the vehicle's type
        @param truck_id: the id of the vehicle whose travel time we want to save
        @param travel_time: the travel time of the specified vehicle
        @param total_waiting_time: the total time the specified vehicle had to wait
        @param created_by: the id of the source that creates the specified vehicle
        @param removed_at: the id of the sink that removes the specified vehicle
        @param type: the type of the specified vehicle
        """
        new_row = pd.Series(data=[truck_id, travel_time, total_waiting_time, created_by, removed_at, type],
                            index=self.travel_time_df_columns)
        self.travel_time_df = self.travel_time_df.append(new_row, ignore_index=True)

    def insert_waiting_time(self, truck_id, bridge_id, waiting_time, type=None):
        """
        Saves the specified waiting time of the given vehicle at the given bridge and the vehicle's type
        @param truck_id: the id of the vehicle whose waiting time we want to save
        @param bridge_id: the id of the bridge where the given vehicle has waited
        @param waiting_time: the waiting time of the given vehicle
        @param type: the type of the specified vehicle
        """
        new_row = pd.Series(data=[truck_id, bridge_id, waiting_time, type], index=self.waiting_time_df_columns)
        self.waiting_time_df = self.waiting_time_df.append(new_row, ignore_index=True)

    def get_travel_time(self):
        """
        Returns a copy of the collected information about the travel time of the vehicles generated in the model and their total waiting time, along
        with the source that created the specified vehicle and the sink that removed it and the vehicle's type
        @return: a Pandas.DataFrame containing the information about vehicles travel time and their total waiting time
        """
        return self.travel_time_df.copy(deep=True)

    def get_waiting_time(self):
        """
        Returns a copy of the collected information about the waiting time of the vehicles generated in the model and their type
        @return: a Pandas.DataFrame containing the information about vehicles waiting time
        """
        return self.waiting_time_df.copy(deep=True)

# EOF -----------------------------------------------------------
