from os import path
import json

default_options = """{
    "url": "http://scoreboard2.uscyberpatriot.org/index.php",
    "team_url": "http://scoreboard2.uscyberpatriot.org/team.php?team=",
    "competition_id": "CCVI",
    "round": 1,
    "round1_filename": "Round1.csv",
    "round1_senior_images":2,
    "round2_filename": "Round2.csv",
    "round2_senior_images":3,
    "round3_filename": "Round3.csv",
    "round3_senior_images":3,
    "division_filename": "Division.csv",
    "response_filename": "Web/response.html",
    "database": "sqlite.db",
    "categories": {"1":"Junior","2":"Senior"},
    "divisions": ["","All Boys","Mixed Gender","All Girls","Cadets"],
    "totals_template": "TotalsTemplate.html",
    "totals": "Totals.csv",
    "totals_web": "Web/Totals.html",
    "junior_totals": "JuniorTotals.csv",
    "junior_totals_web": "Web/JuniorTotals.html",
    "senior_totals": "SeniorTotals.csv",
    "senior_totals_web": "Web/SeniorTotals.html",
    "index_template": "indexTemplate.html",
    "index_web": "Web/index.html"
}"""

def load_options(filename):
    if not path.exists(filename):
        f = open(filename, "w")
        f.write(default_options)
        f.close()
    f = open(filename, "r")
    json_data = f.read()
    f.close()
    return json.loads(json_data)
