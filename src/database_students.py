#!/usr/bin/python
import re
from database_timeline import month_indexed
from fetch_data import read_sheet


database = []
contestant_grouped = {}
contestant_history = {}
month_grouped = {}


tab_name = ["Contest Database", "MODSMO Database"]
sheet_range = ["A3:P", "A3:S"]
scores_ix = [[8, 9, 10, 11], [9, 10, 11, 12, 13, 14]]
width = [16, 19]
anonymity_ix = [6, 7]


def is_valid(row, index):
    res = row and re.fullmatch(r"\d\d\d\d-\d\d-.+", row[0])
    res = res and (row[0][:7] in month_indexed)
    res = res and re.fullmatch(r"\d+", row[1])
    res = res and re.fullmatch(r".+#\d\d\d\d", row[scores_ix[index][0]-1])

    for i in scores_ix[index]:
        res = res and re.fullmatch(r"\d+", row[i])

    res = res and re.fullmatch(r"\d+", row[scores_ix[index][-1]+1])
    res = res and re.fullmatch(r"\d+", row[scores_ix[index][-1]+2])

    return bool(res)


for index in range(2):
    for row in read_sheet(tab_name[index], sheet_range[index]):
        if not is_valid(row, index):
            continue

        entry = {
            "month": row[0][:7],
            "user-id": row[1],
            "name": row[scores_ix[index][0]-1],
            "scores": [int(row[i]) for i in scores_ix[index]],
            "total_score": int(row[scores_ix[index][-1]+1]),
            "rank": int(row[scores_ix[index][-1]+2]),
            "contest_name": month_indexed[row[0][:7]]["name"],
            "medal": row[-1][0] if len(row) == width[index] else "",
            "is_anonymous": row[anonymity_ix[index]] == "Yes"
        }

        if entry["month"] == "2019-05" and entry["is_anonymous"]:
            continue

        database.append(entry)
        if entry["user-id"] not in contestant_grouped:
            contestant_grouped[entry["user-id"]] = []
        contestant_grouped[entry["user-id"]].append(entry)
        if entry["month"] not in month_grouped:
            month_grouped[entry["month"]] = []
        month_grouped[entry["month"]].append(entry)

    for contestant, entries in contestant_grouped.items():
        contestant_history[contestant] = {
            "G": 0, "S": 0, "B": 0, "H": 0, "P": 0
        }
        for entry in entries:
            contestant_history[contestant][entry["medal"] or "P"] += 1

for _, entries in contestant_grouped.items():
    entries.sort(key=lambda entry: entry["month"], reverse=True)

for month, entries in month_grouped.items():
    if month != "2019-05" and month_indexed[month]["p_student"] and \
       int(month_indexed[month]["p_student"]) != len(entries):
        raise Exception(f"Number of participants in {month} does not match")
    entries.sort(key=lambda entry: entry["rank"])