import pandas as pd
import numpy as np
import re

from feature_ids import coupe_type_ids, fuel_type_ids, position_of_cylinders_ids, number_of_gears_ids

df_old = pd.read_csv("http://localhost:8080/data-full.csv")

# drop null rows
df = df_old.drop(columns=['fuel_consumption_combined', 'minimum_turning_circle', 'modification'])

# drop duplicates
df = df.drop_duplicates(subset=['brand', 'model'], keep="last")



def generate_hashtag(row):

    brand, model, generation = row['brand'], row['model'], row['generation']

    brand = re.sub('[^0-9a-z]', '', brand.lower())

    model = re.sub('[^0-9a-z]', '', model.lower())

    generation = re.sub('[^0-9a-z]', '', generation.lower().split(" ")[0])

    hashtags = ['#'+brand+model, '#'+model, '#'+brand[0]+model, '#'+model+generation, '#'+brand+model+generation, '#'+brand[0]+model+generation]

    return "|".join(hashtags)

def convert_data(row):
    """
    Handles only conversion to number type
    """

    #define global dataframe
    global coupe_type_ids, fuel_type_ids, number_of_gears_ids

    # set abs to 1 if yes else 0
    row['abs'] = 0 if row.isnull()['abs'] else 1

    # replace coupe_type with corresponding id
    if not row.isnull().coupe_type:

         # remove any trailing or leading spaces
        ct = row['coupe_type'].strip()

        # replace with id
        row['coupe_type'] = coupe_type_ids[ct] if ct in coupe_type_ids.keys() else coupe_type_ids['Other']

    # remove unit from cylinder_bore (unit is mm.) if not null
    if not row.isnull().cylinder_bore:

        #remove unit
        row['cylinder_bore'] = float(re.sub('mm.','',row['cylinder_bore']).strip())
    
    # remove unit from fuel_tank_volume (unit is litre)
    if not row.isnull().fuel_tank_volume:

        # remove anything inside brackers
        ft = re.sub(r"\(.*\)", "", row['fuel_tank_volume'])
            
        # remove unit
        ft = re.sub('l', '', ft).strip()

        # handle values like 55-60
        ft = re.sub(r".*\-",'', ft).strip()

        # handle values like 95+64
        row['fuel_tank_volume'] = sum(map(float, ft.split('+'))) if ft.find('+') != -1 else float(ft)
    
    # replace fuel_type with corresponding id
    if not row.isnull().fuel_type:

        # remove any trailing or leading spaces
        ft = row['fuel_type'].strip()

        # replace with id
        row['fuel_type'] = fuel_type_ids[ft] if ft in fuel_type_ids.keys() else fuel_type_ids['Other']
    
    # remove unit from kerb_weight (unit is kg.)
    if not row.isnull().kerb_weight:

        # remove values like 1604-1609 select the last value
        kw = re.sub(r".*[-\/]","",row['kerb_weight'])

        # remove unit
        kw = re.sub("kg.", "", kw)

        # remove any more unnecessar characters
        row['kerb_weight'] = float(re.sub(r"[^0-9\.]","",kw).strip())
    
    # remove unit from piston_stroke (unit is mm.)
    if not row.isnull().piston_stroke:

        # remove unit
        row['piston_stroke'] = float(re.sub("mm.","",row['piston_stroke']).strip())

    # replace position_of_cylinders with id
    if not row.isnull().position_of_cylinders:

        # remove any trailing or leading spaces
        poc = row['position_of_cylinders'].strip()

        # replace with id
        row['position_of_cylinders'] = position_of_cylinders_ids[poc] if poc in position_of_cylinders_ids.keys() else position_of_cylinders_ids['Other']
    
    # take only value in unit hp of power
    if not row.isnull().power:

        # remove the rpm part from value if any
        hp_only = re.sub(r"/.*","",row['power'])

        # remove unit (unit is hp)
        row['power'] = float(re.sub(r'[^0-9\.]', '', hp_only).strip())
    
    # take only Nm value of torque
    if not row.isnull().torque:

        # remove rpm part from value if any
        nm_only = re.sub(r"/.*","",row['torque'])

        # remove anythin inside brackers
        nm_only = re.sub(r"(\[|\().*(\]|\))","",nm_only)

        # remove unit and any other unwanted characters (unit is Nm)
        row['torque'] = float(re.sub(r"[^0-9\.]", "", nm_only).strip())
    
    # remove unit from wheelbase
    if not row.isnull().wheelbase:

        # handle values like 2711/2710 mm. take only second value
        wb = re.sub(r".*(/|-)", "", row['wheelbase'])

        # remove unit (unit is mm.)
        row['wheelbase'] = float(re.sub('mm.','',wb).strip())

    # convert doors to int
    if not row.isnull().doors:
        row['doors'] = int(row['doors'])
    
    # convert number_of_cylinders to int
    if not row.isnull().number_of_cylinders:
        row['number_of_cylinders'] = int(row['number_of_cylinders'])

    # convert number_of_gears to int
    if not row.isnull().number_of_gears:

        # handles values with '+'
        ng = str(sum(map(int, row['number_of_gears'].split("+")))) if (row['number_of_gears'].find('+') != -1) else row["number_of_gears"]

        if ng in number_of_gears_ids.keys():
            row['number_of_gears'] = number_of_gears_ids[ng]
        else :
            ng = re.sub(r"[^0-9]", "", row['number_of_gears']).strip()

            if ng in number_of_gears_ids.keys():
                row['number_of_gears'] = number_of_gears_ids[ng]
            else:
                row['number_of_gears'] = number_of_gears_ids['Other']

    # convert number_of_valves_per_cylinder to int
    if not row.isnull().number_of_valves_per_cylinder:
        row['number_of_valves_per_cylinder'] = int(row['number_of_valves_per_cylinder'])
    
    # convert seats to int
    if not row.isnull().seats:
        row['seats'] = sum(map(int, row['seats'].split('+'))) if row['seats'].find('+') != -1 else int(row['seats'])

    
    return row

def handle_nans(row):
    """
    Handle missing values in dataset
    """

    global df, coupe_type_ids, fuel_type_ids, position_of_cylinders_ids

    # replace NULL values in compression_ratio with mean value
    # if row.isnull().compression_ratio:
    #     row['compression_ratio'] = round(df.compression_ratio.mean(),2)

    # replace nan as any in coupe_type
    if row.isnull().coupe_type:
        row['coupe_type'] = coupe_type_ids['Any']
    
    # replace missing values in cylinder_bore with mean
    # if row.isnull().cylinder_bore:
    #     row['cylinder_bore'] = round(df.cylinder_bore.mean(), 1)
    
    # replace missing values in doors with mode
    if row.isnull().doors:
        row['doors'] = df.doors.mode().values[0]
    
    # replace missing values in fuel tank volume with mean
    # if row.isnull().fuel_tank_volume:
    #     row['fuel_tank_volume'] = round(df.fuel_tank_volume.mean())
    
    # replace nan as any in fuel_type
    if row.isnull().fuel_type:
        row['fuel_type'] = fuel_type_ids['Any']

    # replace missing kerb weight with mean value
    # if row.isnull().kerb_weight:
    #     row['kerb_weight'] = round(df.kerb_weight.mean())
    
    # replace missing value in number_of_cylinders with mode
    # if row.isnull().number_of_cylinders:
    #     row['number_of_cylinders'] = df.number_of_cylinders.mode().values[0]

    # replace missing value in number_of_gears with mode
    if row.isnull().number_of_gears:
        row['number_of_gears'] = df.number_of_gears.mode().values[0]
    
    # replace missing value in number_of_valves_per_cylinder with mode
    # if row.isnull().number_of_valves_per_cylinder:
    #     row['number_of_valves_per_cylinder'] = df.number_of_valves_per_cylinder.mode().values[0]

    # replace missing values in piston_stroke with mean
    # if row.isnull().piston_stroke:
    #     row['piston_stroke'] = round(df.piston_stroke.mean(),1)
    
    # replace nan with any in position_of_cylinders
    if row.isnull().position_of_cylinders:
        row['position_of_cylinders'] = position_of_cylinders_ids['Any']
    
    # replace mising values in power with mean
    # if row.isnull().power:
    #     row['power'] = round(df.power.mean())
    
    # replace missing values in seats with mode
    if row.isnull().seats:
        row['seats'] = df.seats.mode().values[0]

    # replace missing values in torque with mean
    # if row.isnull().torque:
    #     row['torque'] = round(df.torque.mean())
    
    # replace missing values in wheelbase with mean
    # if row.isnull().wheelbase:
    #     row['wheelbase'] = round(df.wheelbase.mean())
    
    return row

# convert dataframe to numeric values for possible columnsra
df = df.transform(lambda row: convert_data(row), axis=1)

df_rel = df.copy()
# create a dataset to study relation
df_rel.dropna().to_csv("datasets/out_relation.csv")

# generate hashtags
df['hashtags'] = df.apply(lambda row: generate_hashtag(row), axis=1)

# manage missing values
df = df.transform(lambda row: handle_nans(row), axis=1)

# drop rows with lot of nans
df = df.dropna(thresh=18)

df.to_csv("datasets/out.csv")



