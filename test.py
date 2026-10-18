import pandas as pd

candidates = pd.read_excel("2025MayoralCandidates.xlsx")

print(candidates.columns.tolist())
print(candidates.head(20))