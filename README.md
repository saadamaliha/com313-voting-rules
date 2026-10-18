# Would a candidate win under any voting rule? NYC 2025 Mayoral Primary

We took the real ranked ballots from the 2025 NYC Democratic mayoral primary and counted them under five different voting rules. The question: does the same candidate win no matter which rule you use?


**Public site:** - https://ivynjuguna.github.io/voting-rule-interactive-website/#/

The site has a home page that explains the project, plus one page for each rule with a short explanation and an interactive simulation. You can remove candidates and re-run the count, change the Borda point weights, step through the ranked-choice rounds, and test how voter order affects plurality veto.

## What we did

1. **Collected the ballots.** We used the NYC Board of Elections cast vote records for the June 24, 2025 primary. They come as many Excel files split by ballot type (early voting, election day, affidavit, emergency, other).
2. **Merged them.** `merge.py` keeps only each ballot's five mayoral choices and writes one CSV per ballot type. `merge_categories.py` combines those into a master file.
3. **Filtered to complete ballots.** `filter.py` keeps ballots that ranked five different candidates and drops blanks, overvotes, undervotes, and repeated candidates. That leaves **513,012 ballots** (26,117 distinct rankings) across 12 options (11 candidates plus write-ins).
4. **Coded five voting rules** in Python, one script each.
5. **Stress-tested plurality veto,** since its outcome can depend on the order voters are processed. `plurality_veto_order.py` runs 50 random voter orders.
6. **Built the website** so anyone can explore the same results interactively.

Candidate names come from the Board of Elections candidate list (`2025MayoralCandidates.xlsx`, which maps each CandidacyID to a ballot name). The ballot data itself only contains the numeric IDs.

## The five rules

| Rule | How it picks a winner | Script |
|---|---|---|
| Plurality | Most first-choice votes wins. | `plurality.py` |
| Borda count | Rank 1 gets 5 points down to 1 point for rank 5. Highest total wins. | `borda.py` |
| Copeland | Every pair of candidates is compared head to head. Most pairwise wins takes it. A candidate who beats everyone is a Condorcet winner. | `copeland.py` |
| Ranked choice (STV) | Count each ballot for its top remaining choice. If nobody has a majority, eliminate the last-place candidate and transfer their ballots. | `stv.py` |
| Plurality veto | Each voter vetoes their lowest-ranked active candidate. Candidates at zero are eliminated and the last one standing wins. | `plurality_veto.py` |

For Copeland, a ranked candidate beats an unranked one, and ballots that rank neither are skipped. For plurality veto, voters only ranked five candidates, so unranked candidates are placed below the ranked ones in random order (fixed seed for reproducibility). That random order is a modeling convention, not a claim about what voters want.

## Results

Zohran Mamdani wins under all five rules.

- **Plurality:** Mamdani 315,032 first-choice votes, then Cuomo 84,076 and Lander 69,231.
- **Borda:** Mamdani 1,909,843, Lander 1,640,352, Adams 1,159,976. Cuomo, second in first-choice votes, falls to fifth.
- **Copeland:** Mamdani wins all 11 head-to-head matchups, so he is a Condorcet winner. Lander is second with 10.
- **Ranked choice:** Mamdani holds a majority (61.41%) in round one, so no eliminations are needed.
- **Plurality veto:** Mamdani wins in the main run and in all 50 voter-order tests.

One pattern worth noting: Cuomo has solid first-choice support but ranks low on many ballots, so he does much better under plurality than under Borda or Copeland.

## Limitations

- The dataset only includes ballots that ranked five distinct candidates, about half of the primary's ballots. Voters who ranked deeply are not a random sample of the electorate. For comparison, Mamdani's official first-round share was 43.8%, while it is 61.4% in this filtered data.
- The results describe this filtered group of voters, not the whole city.
- Ties in STV elimination are broken by smallest candidate ID, and the veto test depends on one fixed way of completing partial ballots.
- The website runs plurality veto slightly differently from the Python script. It picks a random unranked candidate to veto directly instead of shuffling a full completed ballot. The distribution is the same, but a given seed will not reproduce the same run as the script.

## Running the code

Put `NYC_2025_Mayor_Filtered.csv` in the same folder as the scripts, then:

```
pip install pandas
python plurality.py
python borda.py
python copeland.py
python stv.py
python plurality_veto.py
python plurality_veto_order.py
```

Each script prints its results and saves a `.txt` file. `merge.py` and `merge_categories.py` need the raw Board of Elections Excel files and the folder path inside them edited to match your computer.

## Files

- `index.html`: the whole website in one self-contained file (no outside dependencies)
- `merge.py`, `merge_categories.py`, `filter.py`: data preparation
- `plurality.py`, `borda.py`, `copeland.py`, `stv.py`, `plurality_veto.py`, `plurality_veto_order.py`: the voting rules
- `*_result.txt`, `plurality_veto_order_test.txt`: saved outputs
- `NYC_2025_Mayor_Filtered.csv`: the filtered ballots

## Data sources

- NYC Board of Elections, 2025 Primary Election cast vote records and candidate list
