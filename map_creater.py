import pickle
from feature_ids import coupe_type_ids, fuel_type_ids, position_of_cylinders_ids, number_of_gears_ids

def create_interval(arr, unit):
    """
    Create list of interval from list of lowerbound
    """

    length = len(arr)

    intervals = {}

    for i in range(length):

        intervals[i] = "{0} {2} - {1} {2}".format(arr[i], arr[i+1], unit) if i+1 < length else "{0} {1} +".format(arr[i], unit)
        
    return intervals

# get the bins
binFile = open('bins', 'rb')
binData = pickle.load(binFile)
binFile.close()

# units
UNITS = {
    'cylinder_bore': 'mm',
    'fuel_tank_volume': 'L',
    'kerb_weight': 'kg',
    'power': 'hp',
    'torque': 'Nm',
    'wheelbase': 'mm',
}

# start creating map
MAP_IDS = {}

# convert bins to corresponding interval strings

for feature, bins in binData.items():

    MAP_IDS[feature] = create_interval(bins, UNITS[feature] if feature in UNITS.keys() else '')

# inverse map ids to column values
feats = {
    'coupe_type':coupe_type_ids,
    'fuel_type':fuel_type_ids, 
    'position_of_cylinders':position_of_cylinders_ids,
    'number_of_gears': number_of_gears_ids
}

for feature, id_map in feats.items():

    MAP_IDS[feature] = {v:k for k,v in id_map.items()}

# pickle the map to mappings
mappingFile = open('mappings', 'wb')

MAP_IDS['abs'] = {0: 'NO', 1: 'YES'}

print(MAP_IDS)

pickle.dump(MAP_IDS, mappingFile)

mappingFile.close()