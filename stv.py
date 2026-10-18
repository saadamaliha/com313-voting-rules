"""
SINGLE TRANSFERABLE VOTE (STV)

Logic:
Under STV, each voter supports their highest-ranked candidate
who is still in the election.

In each round:
1. Count the first available choice on every ballot.
2. If a candidate has more than 50% of the active votes, that
   candidate wins.
3. Otherwise, eliminate the candidate with the fewest votes.
4. Ballots that supported the eliminated candidate transfer to
   their next highest-ranked candidate who is still active.
5. Repeat until a candidate wins.

This script:
1. Loads the filtered NYC mayoral ballot dataset.
2. Converts each row into a ranked ballot.
3. Runs STV round by round.
4. Prints the vote totals and eliminated candidate in each round.
5. Prints the final STV winner.
6. Saves the full round-by-round results to a text file.
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


def stv(ballots):

    # Find all candidates
    active_candidates = set(
        candidate
        for ballot in ballots
        for candidate in ballot
    )

    round_results = []

    round_number = 1

    while len(active_candidates) > 1:

        votes = Counter()

        # Count each ballot's highest-ranked active candidate
        for ballot in ballots:

            for candidate in ballot:

                if candidate in active_candidates:
                    votes[candidate] += 1
                    break

        # Make sure candidates with zero votes still appear
        for candidate in active_candidates:
            if candidate not in votes:
                votes[candidate] = 0

        total_active_votes = sum(votes.values())

        # Sort results from highest to lowest
        sorted_votes = sorted(
            votes.items(),
            key=lambda x: x[1],
            reverse=True
        )

        round_results.append({
            "round": round_number,
            "votes": sorted_votes.copy()
        })

        print(f"\nROUND {round_number}")

        for candidate, count in sorted_votes:
            percentage = (count / total_active_votes) * 100

            print(
                candidate,
                count,
                f"({percentage:.2f}%)"
            )

        # Check whether anyone has a majority
        winner, winner_votes = sorted_votes[0]

        if winner_votes > total_active_votes / 2:

            return winner, round_results

        # Find lowest vote total
        lowest_votes = min(votes.values())

        lowest_candidates = [
            candidate
            for candidate, count in votes.items()
            if count == lowest_votes
        ]

        # Deterministic tie-breaking:
        # eliminate the candidate with the smallest ID
        eliminated = sorted(lowest_candidates)[0]

        print(
            "Eliminated:",
            eliminated
        )

        round_results[-1]["eliminated"] = eliminated

        active_candidates.remove(eliminated)

        round_number += 1


    # If only one candidate remains
    winner = next(iter(active_candidates))

    return winner, round_results


winner, round_results = stv(ballots)


print("\nSTV WINNER:", winner)


# Save results to file
with open("stv_result.txt", "w") as file:

    file.write("STV RESULTS\n\n")

    for result in round_results:

        file.write(
            f"ROUND {result['round']}\n"
        )

        total_votes = sum(
            count
            for candidate, count in result["votes"]
        )

        for candidate, count in result["votes"]:

            percentage = (
                count / total_votes
            ) * 100

            file.write(
                f"{candidate}: {count} "
                f"({percentage:.2f}%)\n"
            )

        if "eliminated" in result:

            file.write(
                f"Eliminated: "
                f"{result['eliminated']}\n"
            )

        file.write("\n")

    file.write(
        f"STV winner: {winner}\n"
    )


print(
    "\nResults saved to stv_result.txt"
)