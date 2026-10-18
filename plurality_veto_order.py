"""
PLURALITY VETO - VOTER ORDER SENSITIVITY TEST

Purpose:
Plurality Veto can depend on the order in which voters are processed.
This script tests whether changing voter order changes the winner.

For each run:
1. Load the filtered NYC mayoral ballot dataset.
2. Keep each voter's five observed rankings.
3. Randomly order the candidates that voter did not rank so that
   Plurality Veto has a complete ranking to work with.
4. Shuffle the order of all voters using a different seed.
5. Run Plurality Veto.
6. Record the winner and elimination order.

After all runs:
- Save the winner from every run.
- Save the elimination order from every run.
- Count how often each candidate wins.

The fixed completion seed keeps the treatment of unranked candidates
the same across runs. Only voter order changes from run to run.
"""

import pandas as pd
from collections import Counter
import random


# --------------------------------------------------
# 1. SETTINGS
# --------------------------------------------------

NUM_RUNS = 50

# Fixed seed used to complete partial rankings
COMPLETION_SEED = 42


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

# Convert dataframe into list of ballots
ballots = df[rank_cols].values.tolist()


# --------------------------------------------------
# 3. FIND ALL CANDIDATES
# --------------------------------------------------

candidates = sorted(
    set(
        candidate
        for ballot in ballots
        for candidate in ballot
    )
)

print("Number of candidates:", len(candidates))
print("Number of ballots:", len(ballots))


# --------------------------------------------------
# 4. COMPLETE PARTIAL BALLOTS
# --------------------------------------------------

def complete_ballots(ballots, candidates, seed):

    rng = random.Random(seed)

    completed = []

    for ballot in ballots:

        # Find candidates not ranked by this voter
        unranked = [
            candidate
            for candidate in candidates
            if candidate not in ballot
        ]

        # Randomly order only the unranked candidates
        rng.shuffle(unranked)

        # Preserve observed rankings first
        complete_ballot = ballot + unranked

        completed.append(complete_ballot)

    return completed


# Use the SAME completed rankings for every order test
completed_ballots = complete_ballots(
    ballots,
    candidates,
    COMPLETION_SEED
)


# --------------------------------------------------
# 5. PLURALITY VETO FUNCTION
# --------------------------------------------------

def plurality_veto(ballots, candidates):

    active_candidates = set(candidates)

    # Initial score = first-place vote count
    scores = Counter()

    for ballot in ballots:
        scores[ballot[0]] += 1

    # Make sure all candidates exist in scores
    for candidate in candidates:
        if candidate not in scores:
            scores[candidate] = 0

    elimination_order = []

    # Eliminate candidates starting with zero score
    for candidate in list(active_candidates):

        if scores[candidate] == 0:

            active_candidates.remove(candidate)

            elimination_order.append(candidate)


    # Process voters one at a time
    for ballot in ballots:

        # Stop once one candidate remains
        if len(active_candidates) == 1:
            break

        veto_candidate = None

        # Find lowest-ranked candidate
        # who is still active
        for candidate in reversed(ballot):

            if candidate in active_candidates:

                veto_candidate = candidate
                break

        if veto_candidate is None:
            continue

        # Apply veto
        scores[veto_candidate] -= 1

        # Eliminate once score reaches zero
        if scores[veto_candidate] <= 0:

            active_candidates.remove(
                veto_candidate
            )

            elimination_order.append(
                veto_candidate
            )


    # Determine winner
    if len(active_candidates) == 1:

        winner = next(iter(active_candidates))

    else:

        winner = None

    return winner, elimination_order


# --------------------------------------------------
# 6. RUN VOTER ORDER TESTS
# --------------------------------------------------

run_results = []

winner_counts = Counter()

for order_seed in range(1, NUM_RUNS + 1):

    print(
        f"Running voter order test "
        f"{order_seed}/{NUM_RUNS}"
    )

    # Create reproducible voter-order shuffle
    rng = random.Random(order_seed)

    shuffled_ballots = completed_ballots.copy()

    rng.shuffle(shuffled_ballots)

    # Run Plurality Veto
    winner, elimination_order = plurality_veto(
        shuffled_ballots,
        candidates
    )

    # Save results from this run
    run_results.append({
        "run": order_seed,
        "seed": order_seed,
        "winner": winner,
        "elimination_order": elimination_order
    })

    winner_counts[winner] += 1


# --------------------------------------------------
# 7. PRINT SUMMARY
# --------------------------------------------------

print("\nPLURALITY VETO ORDER TEST RESULTS\n")

for candidate, count in winner_counts.most_common():

    percentage = (
        count / NUM_RUNS
    ) * 100

    print(
        candidate,
        count,
        f"({percentage:.2f}%)"
    )


# --------------------------------------------------
# 8. SAVE RESULTS TO FILE
# --------------------------------------------------

with open(
    "plurality_veto_order_test.txt",
    "w"
) as file:

    file.write(
        "PLURALITY VETO - VOTER ORDER "
        "SENSITIVITY TEST\n\n"
    )

    file.write(
        f"Number of runs: {NUM_RUNS}\n"
    )

    file.write(
        f"Completion seed: {COMPLETION_SEED}\n\n"
    )


    # ----------------------------------------------
    # Individual run results
    # ----------------------------------------------

    file.write(
        "RESULT OF EACH RUN\n\n"
    )

    for result in run_results:

        file.write(
            f"Run {result['run']}\n"
        )

        file.write(
            f"Order seed: "
            f"{result['seed']}\n"
        )

        file.write(
            f"Winner: "
            f"{result['winner']}\n"
        )

        file.write(
            "Elimination order: "
        )

        file.write(
            " -> ".join(
                result["elimination_order"]
            )
        )

        file.write("\n\n")


    # ----------------------------------------------
    # Winner frequency
    # ----------------------------------------------

    file.write(
        "WINNER FREQUENCY\n\n"
    )

    for candidate, count in winner_counts.most_common():

        percentage = (
            count / NUM_RUNS
        ) * 100

        file.write(
            f"{candidate}: "
            f"{count}/{NUM_RUNS} "
            f"({percentage:.2f}%)\n"
        )


print(
    "\nResults saved to "
    "plurality_veto_order_test.txt"
)