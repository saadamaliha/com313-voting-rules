"""
PLURALITY VETO

Logic:
Each candidate starts with a score equal to their number of
first-place votes.

Voters are then processed one at a time. Each voter vetoes their
lowest-ranked candidate who is still active. When a candidate's
score reaches zero, that candidate is eliminated. The last
remaining candidate wins.

Handling partial rankings:
NYC voters can rank at most five candidates, even though there
are more candidates in the election. Plurality Veto assumes a
complete ranking of all candidates.

To apply the rule to the NYC data:
- The five observed rankings are kept exactly as submitted.
- All unranked candidates are placed below the ranked candidates.
- The unranked candidates are randomly ordered.
- A fixed random seed is used so that the same completed rankings
  are produced every time the program runs.

The random ordering does NOT represent the voter's actual
preferences. It is an implementation convention needed because
the ballot does not tell us how the voter ranks unranked candidates.

This script:
1. Loads the filtered NYC mayoral ballot dataset.
2. Finds all candidates in the election.
3. Completes each partial ballot by randomly ordering its
   unranked candidates.
4. Calculates initial Plurality scores.
5. Processes one veto per voter.
6. Eliminates candidates when their score reaches zero.
7. Prints and saves the elimination order and winner.
"""

import pandas as pd
from collections import Counter
import random


# --------------------------------------------------
# 1. SETTINGS
# --------------------------------------------------

RANDOM_SEED = 55

random_generator = random.Random(RANDOM_SEED)


# --------------------------------------------------
# 2. LOAD FILTERED DATASET
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

# Convert candidate IDs to strings
for col in rank_cols:
    df[col] = df[col].astype(str)

# Convert dataframe into ballots
ballots = df[rank_cols].values.tolist()


# --------------------------------------------------
# 3. PLURALITY VETO
# --------------------------------------------------

def plurality_veto(ballots):

    # Find every candidate appearing in the election
    candidates = sorted(
        set(
            candidate
            for ballot in ballots
            for candidate in ballot
        )
    )

    active_candidates = set(candidates)


    # --------------------------------------------------
    # Initial Plurality scores
    # --------------------------------------------------

    scores = Counter()

    for ballot in ballots:
        scores[ballot[0]] += 1

    # Make sure candidates with no first-place votes
    # are still included
    for candidate in candidates:
        if candidate not in scores:
            scores[candidate] = 0


    # --------------------------------------------------
    # Eliminate candidates starting with score 0
    # --------------------------------------------------

    elimination_order = []

    for candidate in list(active_candidates):

        if scores[candidate] == 0:

            active_candidates.remove(candidate)

            elimination_order.append(candidate)


    # --------------------------------------------------
    # Process voters one at a time
    # --------------------------------------------------

    for ballot in ballots:

        # Stop once only one candidate remains
        if len(active_candidates) == 1:
            break


        # Candidates the voter did NOT rank
        unranked_candidates = [
            candidate
            for candidate in candidates
            if candidate not in ballot
        ]


        # Randomly order the unranked candidates
        random_generator.shuffle(
            unranked_candidates
        )


        # Complete ranking:
        #
        # observed rankings first
        # followed by randomly ordered unranked candidates
        complete_ballot = (
            ballot
            + unranked_candidates
        )


        # Find voter's lowest-ranked ACTIVE candidate
        veto_candidate = None

        for candidate in reversed(complete_ballot):

            if candidate in active_candidates:

                veto_candidate = candidate
                break


        # Apply veto
        scores[veto_candidate] -= 1


        # Eliminate candidate when score reaches zero
        if scores[veto_candidate] <= 0:

            active_candidates.remove(
                veto_candidate
            )

            elimination_order.append(
                veto_candidate
            )


    # --------------------------------------------------
    # Determine winner
    # --------------------------------------------------

    if len(active_candidates) == 1:

        winner = next(
            iter(active_candidates)
        )

    else:

        winner = None


    return winner, scores, elimination_order


# --------------------------------------------------
# 4. RUN PLURALITY VETO
# --------------------------------------------------

winner, scores, elimination_order = plurality_veto(
    ballots
)


# --------------------------------------------------
# 5. PRINT RESULTS
# --------------------------------------------------

print("PLURALITY VETO RESULTS\n")

print("Random seed:", RANDOM_SEED)

print("\nElimination order:")

for candidate in elimination_order:
    print(candidate)


if winner is not None:

    print(
        "\nPlurality Veto winner:",
        winner
    )

else:

    print(
        "\nNo single winner was produced."
    )


# --------------------------------------------------
# 6. SAVE RESULTS
# --------------------------------------------------

with open(
    "plurality_veto_result.txt",
    "w"
) as file:

    file.write(
        "PLURALITY VETO RESULTS\n\n"
    )

    file.write(
        f"Random seed: {RANDOM_SEED}\n\n"
    )

    file.write(
        "Elimination order:\n"
    )

    for candidate in elimination_order:

        file.write(
            f"{candidate}\n"
        )

    if winner is not None:

        file.write(
            f"\nPlurality Veto winner: "
            f"{winner}\n"
        )

    else:

        file.write(
            "\nNo single winner was produced.\n"
        )


print(
    "\nResults saved to "
    "plurality_veto_result.txt"
)