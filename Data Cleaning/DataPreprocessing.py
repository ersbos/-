import pathlib
import pandas as pd

DATA_DIR = pathlib.Path("C:/Users/umitc/Desktop/python_vscode/Aselsan proje/proje/data/")
df = pd.read_feather(DATA_DIR / "Processed.feather")


# Define the failure periods, Given in the data description
Classification_df = df.copy(deep=True)

failure_periods = [
    ("2022-02-28 21:53", "2022-03-01 02:00"),
    ("2022-03-23 14:54", "2022-03-23 15:24"),
    ("2022-05-30 12:00", "2022-06-02 06:18"),
]

failure_periods = [
    (pd.to_datetime(start), pd.to_datetime(end)) for start, end in failure_periods
]

N_Hours = 2

Classification_df["Target"] = 0

# Iterate through the failure periods and assign labels
for start, end in failure_periods:
    mask = (Classification_df["timestamp"] >= start) & (
        Classification_df["timestamp"] <= end
    )
    Classification_df.loc[mask, "Target"] = 2  # Label as 2 for failure state
    
    two_hours_before_start = start - pd.Timedelta(hours=N_Hours)
    mask = (Classification_df["timestamp"] >= two_hours_before_start) & (
        Classification_df["timestamp"] < start
    )
    Classification_df.loc[mask, "Target"] = 1  # Label as 1 for 2 hours before failure

# Print the first few rows of the updated DataFrame
print(Classification_df.head())


Classification_df.to_feather(DATA_DIR / "Classification.feather")

#regression data frame
Reg_df = df.copy(deep=True)

failure_periods = [
    ("2022-02-28 21:53", "2022-03-01 02:00"),
    ("2022-03-23 14:54", "2022-03-23 15:24"),
    ("2022-05-30 12:00", "2022-06-02 06:18"),
]

failure_periods = [
    (pd.to_datetime(start), pd.to_datetime(end)) for start, end in failure_periods
]

# Sort failure periods by start time
failure_periods.sort(key=lambda x: x[0])

def find_time_till_failure(curr_time):
    for start, end in failure_periods:
        if curr_time < start:
            return (start - curr_time).total_seconds() / 3600
    return 0

# Apply the function to create the "Hours_till_Failure" column
Reg_df["Hours_till_Failure"] = Reg_df["timestamp"].apply(find_time_till_failure)

Reg_df.to_feather(DATA_DIR / "Regression.feather")

#Failure detection data frame
FD_df = df.copy(deep=True)

failure_periods = [
    ("2022-02-28 21:53", "2022-03-01 02:00"),
    ("2022-03-23 14:54", "2022-03-23 15:24"),
    ("2022-05-30 12:00", "2022-06-02 06:18"),
]

failure_periods = [
    (pd.to_datetime(start), pd.to_datetime(end)) for start, end in failure_periods
]

FD_df["Failure"] = 0

for start, end in failure_periods:
    mask = (FD_df["timestamp"] >= start) & (
        FD_df["timestamp"] <= end
    )
    FD_df.loc[mask, "Failure"] = 1

FD_df.to_feather(DATA_DIR / "Failure_detection.feather")