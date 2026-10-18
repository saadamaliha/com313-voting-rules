"""
COPELAND VOTING

Logic:
Under Copeland, every candidate is compared head-to-head against
every other candidate.

For each pair of candidates A and B:

- If both candidates are ranked on a ballot, the candidate ranked
  higher receives that voter's preference.
- If only one of the two candidates is ranked, the ranked candidate
  is preferred because unranked candidates are treated as tied for last.
- If neither candidate is ranked, that ballot does not contribute
  to the comparison.

The candidate who receives more voter preferences in a pairwise
comparison wins that matchup and receives 1 Copeland point.
If the matchup is tied, both candidates receive 0.5 points.

After every pair of candidates has been compared, the candidate
with the highest total Copeland score wins.

A Condorcet winner is a candidate who defeats every other candidate
in a head-to-head comparison.

This script:
1. Loads the filtered NYC mayoral ballot dataset.
2. Converts each row into a ranked ballot.
3. Finds all candidates in the election.
4. Compares every pair of candidates head-to-head.
5. Calculates Copeland scores.
6. Checks whether a Condorcet winner exists.
7. Prints all pairwise results and the final winner.
"""

import pandas as pd
from itertools import combinations


# --------------------------------------------------
# 1. Load filtered dataset
# --------------------------------------------------

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


# --------------------------------------------------
# 2. Convert candidate IDs to strings
# --------------------------------------------------

for col in rank_cols:
    df[col] = df[col].astype(str)


# --------------------------------------------------
# 3. Convert dataframe into ballots
# --------------------------------------------------

ballots = df[rank_cols].values.tolist()


# --------------------------------------------------
# 4. Find all candidates
# --------------------------------------------------

candidates = sorted(
    set(
        candidate
        for ballot in ballots
        for candidate in ballot
    )
)

print("Number of candidates:", len(candidates))


# --------------------------------------------------
# 5. Initialize Copeland scores
# --------------------------------------------------

scores = {
    candidate: 0
    for candidate in candidates
}

pairwise_wins = {
    candidate: 0
    for candidate in candidates
}


# --------------------------------------------------
# 6. Compare every pair of candidates
# --------------------------------------------------

for candidate_a, candidate_b in combinations(candidates, 2):

    a_votes = 0
    b_votes = 0

    for ballot in ballots:

        a_ranked = candidate_a in ballot
        b_ranked = candidate_b in ballot

        # Both candidates are ranked
        if a_ranked and b_ranked:

            if ballot.index(candidate_a) < ballot.index(candidate_b):
                a_votes += 1

            else:
                b_votes += 1

        # A ranked, B unranked
        elif a_ranked and not b_ranked:

            a_votes += 1

        # B ranked, A unranked
        elif b_ranked and not a_ranked:

            b_votes += 1

        # Neither ranked:
        # treat them as tied for last, so this ballot
        # contributes nothing to this pairwise comparison


    print(
        candidate_a,
        "vs",
        candidate_b,
        ":",
        a_votes,
        "-",
        b_votes
    )


    # A wins pairwise comparison
    if a_votes > b_votes:

        scores[candidate_a] += 1
        pairwise_wins[candidate_a] += 1


    # B wins pairwise comparison
    elif b_votes > a_votes:

        scores[candidate_b] += 1
        pairwise_wins[candidate_b] += 1


    # Pairwise tie
    else:

        scores[candidate_a] += 0.5
        scores[candidate_b] += 0.5


# --------------------------------------------------
# 7. Find Copeland winner
# --------------------------------------------------

winner = max(
    scores,
    key=scores.get
)


# --------------------------------------------------
# 8. Check for Condorcet winner
# --------------------------------------------------

condorcet_winner = None

for candidate in candidates:

    # A Condorcet winner must defeat all other candidates
    if pairwise_wins[candidate] == len(candidates) - 1:

        condorcet_winner = candidate
        break


# --------------------------------------------------
# 9. Print final results
# --------------------------------------------------

print("\nCOPELAND RESULTS\n")

for candidate, score in sorted(
    scores.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(candidate, score)


print("\nCopeland winner:", winner)


if condorcet_winner is not None:

    print(
        "Condorcet winner:",
        condorcet_winner
    )

else:

    print(
        "No Condorcet winner exists."
    )

with open("copeland_result.txt", "w") as file:
    file.write("COPELAND RESULTS\n\n")

    for candidate, score in sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        file.write(f"{candidate}: {score}\n")

    file.write(f"\nCopeland winner: {winner}\n")

    if condorcet_winner is not None:
        file.write(
            f"Condorcet winner: {condorcet_winner}\n"
        )
    else:
        file.write(
            "No Condorcet winner exists.\n"
        )

print("\nResults saved to copeland_result.txt")