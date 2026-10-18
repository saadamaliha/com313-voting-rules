import pandas as pd
import os

folder = r"C:\Users\Sa'ada Malina Umaima\Documents\com313_midterm\datasets"

files = [
    "merged_ABS.csv",
    "merged_EAR.csv",
    "merged_ELE.csv",
    "merged_AFF.csv",
    "merged_EMG.csv",
    "merged_OTH.csv"
]

all_data = []

for file in files:
    path = os.path.join(folder, file)

    print("Reading:", file)

    df = pd.read_csv(path)

    print("Rows:", len(df))

    all_data.append(df)

master = pd.concat(all_data, ignore_index=True)

print("\nTotal ballots:", len(master))
print(master.head())

master.to_csv(
    os.path.join(folder, "NYC_2025_Mayor_Master.csv"),
    index=False
)

print("\nSaved master dataset.")