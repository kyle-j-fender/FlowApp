import pandas as pd
import json

def json_to_dataframe(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Convert the JSON data to a Pandas DataFrame
    df = pd.DataFrame(data)
    return df


def get_closest_value(df, column_name, filter_value):
    # Find the absolute difference between the filter_value and each value in the column
    df['diff'] = (df[column_name] - filter_value).abs()

    # Get the row with the minimum difference
    closest_row = df.loc[df['diff'].idxmin()]

    # Drop the difference column before returning the result
    df.drop(columns=['diff'], inplace=True)

    return closest_row

def get_nominal_kfactor(row):
    nkf = row['Nominal K-Factor'].item()
    return nkf

def get_nominal_kfactor_min(row):
    min = row['K Factor Min'].item()
    return min

def get_nominal_kfactor_max(row):
    max = row['K Factor Max'].item()
    return max

def get_nominal_kfactor_percent(row):
    percent = row['Percent of Nominal K-5.6 Discharge'].item()
    return percent

def get_nominal_kfactor_thread(row):
    thread = row['Thread Type'].item()
    return thread