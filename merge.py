import pandas as pd
import glob
import os

# Folder containing all of your CVR Excel files
folder = r"C:\Users\Sa'ada Malina Umaima\Documents\com313_midterm\datasets"

# Ballot categories
categories = ["EAR", "ELE", "AFF", "EMG", "OTH"]

# Only keep the mayoral columns we actually need
columns_needed = [
    "Cast Vote Record",
    "DEM Mayor Choice 1 of 5 Citywide (026916)",
    "DEM Mayor Choice 2 of 5 Citywide (226916)",
    "DEM Mayor Choice 3 of 5 Citywide (326916)",
    "DEM Mayor Choice 4 of 5 Citywide (426916)",
    "DEM Mayor Choice 5 of 5 Citywide (526916)"
]

for category in categories:

    print(f"\nProcessing {category} files...")

    # Finds files such as:
    # *_ABS.xlsx
    # *_EAR1.xlsx, *_EAR2.xlsx, ...
    # *_ELE1.xlsx, *_ELE2.xlsx, ...
    files = glob.glob(
        os.path.join(folder, f"*_{category}*.xlsx")
    )

    # Do not include any previously merged files
    files = [
        file for file in files
        if not os.path.basename(file).startswith("merged_")
    ]

    print("Files found:", len(files))

    if len(files) == 0:
        print(f"No {category} files found.")
        continue

    all_data = []

    for file in files:

        print("Reading:", os.path.basename(file))

        try:
            # Read only the 6 mayor columns
            df = pd.read_excel(
                file,
                usecols=columns_needed
            )

            # Add ballot type so we know where it came from
            df["Ballot_Type"] = category

            all_data.append(df)

        except Exception as e:
            print("ERROR reading:", os.path.basename(file))
            print(e)

    # Skip if none of the files worked
    if len(all_data) == 0:
        print(f"No {category} files could be processed.")
        continue

    # Merge all files in the category
    merged = pd.concat(
        all_data,
        ignore_index=True
    )

    # Rename columns to simpler names
    merged = merged.rename(columns={
        "Cast Vote Record": "Ballot_ID",
        "DEM Mayor Choice 1 of 5 Citywide (026916)": "Rank_1",
        "DEM Mayor Choice 2 of 5 Citywide (226916)": "Rank_2",
        "DEM Mayor Choice 3 of 5 Citywide (326916)": "Rank_3",
        "DEM Mayor Choice 4 of 5 Citywide (426916)": "Rank_4",
        "DEM Mayor Choice 5 of 5 Citywide (526916)": "Rank_5"
    })

    # Save as CSV instead of Excel
    output_file = os.path.join(
        folder,
        f"merged_{category}.csv"
    )

    merged.to_csv(
        output_file,
        index=False
    )

    print(f"{category} complete!")
    print("Total rows:", len(merged))
    print("Saved as:", output_file)

print("\nFinished merging all categories.")