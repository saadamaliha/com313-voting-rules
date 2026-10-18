"""
BORDA COUNT

Logic:
Under Borda, candidates receive points based on their position
in each voter's ranking.

Since the filtered dataset contains five ranked candidates per ballot:

Rank 1 = 5 points
Rank 2 = 4 points
Rank 3 = 3 points
Rank 4 = 2 points
Rank 5 = 1 point

The points from all ballots are added together, and the candidate
with the highest total score wins.

This script:
1. Loads the filtered NYC mayoral ballot dataset.
2. Converts each row into a ranked ballot.
3. Assigns Borda points to each ranked candidate.
4. Adds the scores across all ballots.
5. Prints the final scores and the Borda winner.
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


def borda(ballots):

    scores = Counter()

    # Borda points:
    # Rank 1 = 5
    # Rank 2 = 4
    # Rank 3 = 3
    # Rank 4 = 2
    # Rank 5 = 1

    points = [5, 4, 3, 2, 1]

    for ballot in ballots:

        for i in range(5):

            candidate = ballot[i]

            scores[candidate] += points[i]

    winner = scores.most_common(1)[0][0]

    return winner, scores


winner, results = borda(ballots)

print("BORDA RESULTS\n")

for candidate, score in results.most_common():
    print(candidate, score)

print("\nBorda winner:", winner)

with open("borda_result.txt", "w") as file:
    file.write("BORDA RESULTS\n\n")

    for candidate, score in results.most_common():
        file.write(f"{candidate}: {score}\n")

    file.write(f"\nBorda winner: {winner}\n")

print("\nResults saved to borda_result.txt")