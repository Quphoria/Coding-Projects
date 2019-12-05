from json_options import load_options
options = load_options("options.json")
files = [[options["totals"],options["totals_web"]],[options["junior_totals"],options["junior_totals_web"]],[options["senior_totals"],options["senior_totals_web"]]]
time_tag = "{TIME}"
row_tag = "<!--{ROW}-->"
row_end = "<!--{/ROW}-->"
data_div_pos = "{DATA_DIV_POS}"
data_pos = "{DATA_POS}"
data_team = "{DATA_TEAM}"
data_category = "{DATA_CAT}"
data_total = "{DATA_TOTAL}"
data_division = "{DATA_DIVISION}"
divisions = options["divisions"]
def getDivPos(div):
    pos = 0
    for position, item in enumerate(divisions):
        if item == div:
            pos = position
    return pos
row_href = "{HREF}"
team_url = options["team_url"]
import datetime
import math
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

index_template_file = open(options["index_template"],"r")
index_file = open(options["index_web"],"w")
index_file.write(index_template_file.read().replace("[[ID]]", options["competition_id"]))
index_template_file.close()
index_file.close()


for file in files:
    print("Opening " + file[0])
    csvfile = open(file[0],"r")

    templatefile = open(options["totals_template"],"r")
    template = templatefile.read()
    templatefile.close()
    GenTime = datetime.datetime.now().strftime("%H:%M:%S&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%A, %B %d, %Y")

    print("Generating HTML")

    csvfiledata = csvfile.readlines()
    csvfile.close()

    try:
        assert csvfiledata[0] == "Team ID,Scored Images Category,Total CCS Score,Division\n"

        template = template.split(row_tag)
        gen_html = template[0].replace(time_tag,GenTime)
        template = template[1].split(row_end)
        row_html = template[0]
        junior_pos = [1,1,1,1,1]
        junior_div_pos = 1
        senior_pos = [1,1,1,1,1]
        senior_div_pos = 1
        for i in range(1,len(csvfiledata)):
            if csvfiledata[i] != "\n" and csvfiledata:
                row_data = csvfiledata[i].replace("\n","").split(",")
                row = row_html.replace(data_team,row_data[0])
                if row_data[1] == options["categories"]["1"]:
                    row = row.replace(data_pos,ordinal(junior_pos[getDivPos(row_data[3].replace("None",""))]))
                    junior_pos[getDivPos(row_data[3].replace("None",""))] += 1
                    row = row.replace(data_div_pos,ordinal(junior_div_pos))
                    junior_div_pos += 1
                else:
                    row = row.replace(data_pos,ordinal(senior_pos[getDivPos(row_data[3].replace("None",""))]))
                    senior_pos[getDivPos(row_data[3].replace("None",""))] += 1
                    row = row.replace(data_div_pos,ordinal(senior_div_pos))
                    senior_div_pos += 1
                row = row.replace(data_category,row_data[1])
                row = row.replace(data_total,row_data[2][:-2])
                row = row.replace(row_href,team_url + row_data[0])
                row = row.replace(data_division,row_data[3].replace("None",""))
                gen_html += row

        gen_html += template[1]

        print("Saving HTML to " + file[1])
        htmlfile = open(file[1],"w")
        htmlfile.write(gen_html)
        htmlfile.close()
    except Exception as ex:
        print("An Error occurred with: " + str(file) + ", Error: " + str(ex))

print("Done.")
