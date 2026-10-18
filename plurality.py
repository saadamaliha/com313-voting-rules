"""
PLURALITY VOTING

# Logic:
Under Plurality, only each voter's first-ranked candidate matters. 
Every ballot gives one vote to its Rank_1 candidate.
The candidate with the most first-place votes wins.

# This script:
1. Loads the filtered NYC mayoral ballot dataset.
2. Converts each row into a ranked ballot.
3. Counts only the first-ranked candidate on each ballot.
4. Prints the vote totals and the Plurality winner.
"""
import pandas as pd
from collections import Counter

# Load filtered dataset
df = pd.read_csv(
    "NYC_2025_Mayor_Filtered.csv",
    low_memory=False
)

rank_cols = [
    "Rank_1",
    "Rank_2",
    "Rank_3",
    "Rank_4",
    "Rank_5"
]

# Convert candidate IDs to strings
for col in rank_cols:
    df[col] = df[col].astype(str)

# Convert dataframe into list of ballots
ballots = df[rank_cols].values.tolist()


def plurality(ballots):

    votes = Counter()

    # Only first choice matters
    for ballot in ballots:
        votes[ballot[0]] += 1

    winner = votes.most_common(1)[0][0]

    return winner, votes


winner, results = plurality(ballots)

print("PLURALITY RESULTS\n")

for candidate, votes in results.most_common():
    print(candidate, votes)

print("\nPlurality winner:", winner)

with open("plurality_result.txt", "w") as file:
    file.write("PLURALITY RESULTS\n\n")

    for candidate, votes in results.most_common():
        file.write(f"{candidate}: {votes}\n")

    file.write(f"\nPlurality winner: {winner}\n")

print("\nResults saved to plurality_result.txt")