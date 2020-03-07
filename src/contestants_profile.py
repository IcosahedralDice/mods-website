#!/usr/bin/python
import sys
import util
import templates
from os import path
from database_students import contestant_history
from database_students import contestant_grouped

def run(name):
    print("Creating contestants/" + name + "/index")
    history = contestant_history[name]
    html = templates.get("contestants/profile")
    html = templates.initial_replace(html, 2) \
            .replace("__NAME__", name) \
            .replace("__GOLD__", str(history["G"])) \
            .replace("__SILVER__", str(history["S"])) \
            .replace("__BRONZE__", str(history["B"])) \
            .replace("__HONOURABLE_MENTION__", str(history["H"])) \
            .replace("__PARTICIPATIONS__", str(sum(history.values())))

    tablehtml = ""
    for row in contestant_grouped[name]:
        rowhtml = templates.get("contestants/profile_row") \
                    .replace("__MONTH__", row["month"]) \
                    .replace("__RANK__", row["rank"])
        if row["medal"] == "G":
            rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/month/individual_gold"))
        elif row["medal"] == "S":
            rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/month/individual_silver"))
        elif row["medal"] == "B":
            rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/month/individual_bronze"))
        elif row["medal"] == "H":
            rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/month/individual_honourable"))
        else:
            rowhtml = rowhtml.replace("__MEDAL__", "")
        tablehtml += rowhtml

    html = html.replace("__TABLE__", tablehtml)
    html = templates.final_replace(html, "../..")
    util.writefile(path.normpath("../contestants/" + name + "/index.html"), html)

if __name__ == "__main__":
    run(sys.argv[1])