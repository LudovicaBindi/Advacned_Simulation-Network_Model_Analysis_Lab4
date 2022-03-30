def read_traffic_probabilities(source='../data/traffic_probabilities.txt'):

    # split the strings
    file_split = []
    with open(source) as f:  # open the file
        for line in f:  # read all the lines in the file
            line = line.rstrip('\n')
            road = line.split(',')[0]  # remove the trailing newline
            vehicle = get_vehicle_prob(line.split(',')[1])
            prob = line.split(',')[2]
            file_split.append([road, vehicle, prob])

    result = {}

    for el in file_split:
        if el[0] in result:
            result[el[0]][el[1]] = el[2]
        else:
            road_dict = {el[1]: el[2]}
            result[el[0]] = road_dict

    return result

def get_vehicle_prob(info):
    vehicle_type = info.split('-')[1]
    if vehicle_type == 'Heavy Truck':
        final_key = 'HeavyTruck'
    elif vehicle_type == 'Medium Truck':
        final_key = 'MediumTruck'
    elif vehicle_type == 'Small Truck':
        final_key = 'SmallTruck'
    elif vehicle_type == 'Large Bus':
        final_key = 'LargeBus'
    else:
        # if vehicle_type == 'Medium Bus'
        final_key = 'MiniBus'

    return final_key


print(read_traffic_probabilities())