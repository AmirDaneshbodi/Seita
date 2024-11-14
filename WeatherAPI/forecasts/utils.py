import pandas as pd

def load_data():
    # Load data from CSV, assuming it's in the root of the Django project
    return pd.read_csv("/Users/adaneshbodi/Library/CloudStorage/OneDrive-Deloitte(O365D)/python_projects/Seita/WeatherAPI/weather_data.csv", parse_dates=["event_start"])


def sunny_treshold(df):
    # Filter rows where 'sensor' is 'irradiance' and the value is higher than zero
    filtered_df = df[(df["sensor"] == "irradiance") & (df["event_value"] > 0)]
    return filtered_df["event_value"].mean()


def windy_treshold(df):
    # Filter rows where 'sensor' is 'irradiance' and the value is higher than zero
    filtered_df = df[(df["sensor"] == "wind speed")]
    return filtered_df["event_value"].mean()


def find_closest_timestamp(data, requested_timestamp):
    # Calculate the time difference between each timestamp and 'requested_timestamp'
    time_diffs = abs(data["event_start"] - requested_timestamp)
    # Get the index of the minimum difference
    closest_index = time_diffs.idxmin()
    # Return the row with the closest timestamp
    return data.loc[closest_index]["event_start"]


if __name__ == "__main__":
    df = load_data()
    print(windy_treshold(df))