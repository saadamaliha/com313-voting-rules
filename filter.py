import pandas as pd

# --------------------------------------------------
# 1. Load clean master dataset
# --------------------------------------------------

df = pd.read_csv("NYC_2025_Mayor_Clean.csv")

rank_cols = [
    "Rank_1",
    "Rank_2",
    "Rank_3",
    "Rank_4",
    "Rank_5"
]

print("Original ballots:", len(df))


# --------------------------------------------------
# 2. Remove ballots with missing ranks
# --------------------------------------------------

filtered = df.dropna(
    subset=rank_cols
).copy()


# --------------------------------------------------
# 3. Convert rankings to clean strings
# --------------------------------------------------

for col in rank_cols:
    filtered[col] = (
        filtered[col]
        .astype(str)
        .str.strip()
    )


# --------------------------------------------------
# 4. Remove ballots containing undervote / overvote
# --------------------------------------------------

invalid_values = {
    "undervote",
    "overvote"
}

def contains_invalid_vote(row):

    for col in rank_cols:

        value = row[col].lower()

        if value in invalid_values:
            return True

    return False


filtered = filtered[
    ~filtered.apply(
        contains_invalid_vote,
        axis=1
    )
].copy()


# --------------------------------------------------
# 5. Keep only ballots with 5 UNIQUE candidates
# --------------------------------------------------

def five_unique_candidates(row):

    rankings = [
        row["Rank_1"],
        row["Rank_2"],
        row["Rank_3"],
        row["Rank_4"],
        row["Rank_5"]
    ]

    return len(set(rankings)) == 5


filtered = filtered[
    filtered.apply(
        five_unique_candidates,
        axis=1
    )
].copy()


# --------------------------------------------------
# 6. Reset row numbers
# --------------------------------------------------

filtered = filtered.reset_index(drop=True)


# --------------------------------------------------
# 7. Show results
# --------------------------------------------------

print("Filtered ballots:", len(filtered))

print(
    "Removed ballots:",
    len(df) - len(filtered)
)

print("\nFirst five filtered ballots:")

print(
    filtered[
        rank_cols
    ].head()
)


# --------------------------------------------------
# 8. Save
# --------------------------------------------------

filtered.to_csv(
    "NYC_2025_Mayor_Filtered.csv",
    index=False
)

print(
    "\nSaved as NYC_2025_Mayor_Filtered.csv"
)