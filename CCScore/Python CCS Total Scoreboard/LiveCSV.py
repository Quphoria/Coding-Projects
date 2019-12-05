import requests, re
from json_options import load_options
options = load_options("options.json")
url = options["url"]
devurl = "http://localhost:8008/index.php"
# url = devurl #Comment for real thing
round_files = {1:options["round1_filename"], 2:options["round2_filename"], 3:options["round3_filename"]}
round_filename = round_files[options["round"]]
division_filename = options["division_filename"]
division_col = False

print("Fetching Url: " + url)

webdata = ""
tries = 0
while tries < 5:
    try:
        webdata = requests.get(url)
        assert webdata.status_code == 200
        webdata = webdata.content.decode()
        try:
            responsefile = open(options["response_filename"],"w")
            responsefile.write(webdata)
            responsefile.close()
        except Exception as ex:
            print("Error when saving response: " + str(ex))
        print("Parsing Webpage")
        webdata = webdata.split("<table cellspacing='0' cellpadding='0' class='CSSTableGenerator'>")[1].split("</table>")[0]
        tries = 6
    except Exception as ex:
        tries += 1
        print("Failed to fetch webpage. [%s/5]" % str(tries))
        print("Error: " + str(ex))
if tries == 5:
    raise Exception("Failed to fetch scoreboard.")


webdata = re.sub('<tr [^>]+>', ' ', webdata).split("</tr>\r\n")

table_headers = re.sub('<td [^>]+>', '', webdata[0]).split("</td>")
header_titles = ["Team<br>Number","Scored<br>Images","CCS<br>Score"]
header_col = [0,0,0]
cur_col = [0,0,0]
if "Division" in table_headers:
    division_col = True
    print("Found Division Column.")
    header_titles.append("Division")
    header_col.append(0)
    cur_col.append(0)
for i in range(len(header_titles)):
    for header in table_headers:
        if header_titles[i] == header:
            header_col[i] = cur_col[i]
        cur_col[i] += 1

if not "href='index.php" in webdata[0]:
    raise Exception("Invalid scoreboard page (not index.php)")

csvfile = open(round_filename,"w")
csvfile.write("Team Number,Scored Images,CCS Score\n")
if division_col:
    divfile = open(division_filename,"w")
    divfile.write("Team Number,Division\n")
# print(webdata)
for i in range(1,len(webdata)):
    row = webdata[i].replace("</td>","").split("<td>")
    if len(row) >= 5:
        csvfile.write("%s,%s,%s\n" % (row[header_col[0]+1],row[header_col[1]+1],row[header_col[2]+1]))
        if division_col:
            divfile.write("%s,%s\n" % (row[header_col[0]+1],row[header_col[3]+1]))
csvfile.close()
if division_col:
    divfile.close()
print("CSV File Saved.")

print("Done.")
