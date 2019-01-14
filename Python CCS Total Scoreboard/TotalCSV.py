import sqlitedb_IO
DB = sqlitedb_IO.DB()
DB.load()
tables = []
divisions = []
got_division = False

# tablename,filename,comp_round,senior_images
rounds = [["Round1","Round1.csv",1,2],["Round2","Round2.csv",2,3],["Round3","Round3.csv",2,3]]
division = ["Division","Division.csv"]

for round in rounds:
    tablename = round[0]
    filename = round[1]
    comp_round = round[2]
    senior_images = round[3]
    tables.append(tablename)
    print("Opening: " + filename)
    try:
        csvfile = open(filename,"r")
        data = []
        csvfiledata = csvfile.readlines()
        csvfile.close()
        try:
            assert csvfiledata[0] == "Team Number,Scored Images,CCS Score\n"
            for i in range(1,len(csvfiledata)):
                row = csvfiledata[i].replace("\n","")
                if row:
                    rowdata = row.split(",")
                    category = 1
                    if int(rowdata[1]) == senior_images:
                        category = 2
                    data.append((rowdata[0],category,rowdata[2],comp_round))
        except Exception as ex:
            print("Invalid CSV file: " + filename + ", Error: " + str(ex))
        try:
            DB.run_sql("""
                DROP TABLE IF EXISTS %s;
            """ % tablename)
        except Exception as ex:
            print("Error when dropping table: " + tablename + ", Error: "+ str(ex))
        DB.run_sql('''CREATE TABLE %s
                      ("Team" text, "Scored Images Category" real, "CCS Score" real, "Round" real)
                ''' % tablename)
        print("Inserting values into DB")
        DB.run_many_sql('INSERT INTO %s VALUES (?,?,?,?)' % tablename, data)
    except Exception as ex:
        print("Error with " + tablename + ", Error: " + str(ex))

tablename = division[0]
filename = division[1]
divisions.append(tablename)
print("Opening: " + filename)
try:
    csvfile = open(filename,"r")
    data = []
    csvfiledata = csvfile.readlines()
    csvfile.close()
    try:
        assert csvfiledata[0] == "Team Number,Division\n"
        for i in range(1,len(csvfiledata)):
            row = csvfiledata[i].replace("\n","")
            if row:
                rowdata = row.split(",")
                data.append((rowdata[0],rowdata[1]))
    except Exception as ex:
        print("Invalid CSV file: " + filename + ", Error: " + str(ex))
    try:
        DB.run_sql("""
            DROP TABLE IF EXISTS %s;
        """ % tablename)
    except Exception as ex:
        print("Error when dropping table: " + tablename + ", Error: "+ str(ex))
    DB.run_sql('''CREATE TABLE %s
                  ("Team" text, "Division" text)
            ''' % tablename)
    print("Inserting values into DB")
    DB.run_many_sql('INSERT INTO %s VALUES (?,?)' % tablename, data)
    got_division = True
except Exception as ex:
    print("Error with " + tablename + ", Error: " + str(ex))

for tablename in tables:
    DB.run_sql('''CREATE TABLE IF NOT EXISTS %s
                  ("Team" text, "Scored Images Category" real, "CCS Score" real, "Round" real)
            ''' % tablename)
for tablename in divisions:
    DB.run_sql('''CREATE TABLE IF NOT EXISTS %s
                  ("Team" text, "Division" text)
            ''' % tablename)

print("Saving DB")
DB.save()
print("Calculating Totals and Saving CSV Files")
totals_sql = """
SELECT un.Team, Max(un.[Scored Images Category]) AS [Max Scored Images Category], Sum(un.[CCS Score]) AS [Total CCS Score]
FROM (
  SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round1]
  UNION SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round2]
  UNION SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round3]
) AS un
GROUP BY un.Team
ORDER BY Sum(un.[CCS Score]) DESC;
"""

totals_category_sql = """
SELECT un.Team, Max(un.[Scored Images Category]) AS [Max Scored Images Category], Sum(un.[CCS Score]) AS [Total CCS Score]
FROM (
  SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round1]
  UNION SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round2]
  UNION SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round3]
) AS un
GROUP BY un.Team
HAVING [Max Scored Images Category] = ?
ORDER BY Sum(un.[CCS Score]) DESC;
"""

totals_sql_div = """
SELECT un2.Team, un2.[Max Scored Images Category], un2.[Total CCS Score], Division.Division
FROM (SELECT un.Team, Max(un.[Scored Images Category]) AS [Max Scored Images Category], Sum(un.[CCS Score]) AS [Total CCS Score]
FROM (
  SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round1]
  UNION SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round2]
  UNION SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round3]
) AS un
GROUP BY un.Team
ORDER BY Sum(un.[CCS Score]) DESC
) AS un2
LEFT JOIN Division ON un2.Team = Division.Team;
"""

# GROUP BY un2.Team
# ORDER BY un2.[Total CCS Score] DESC;

totals_category_sql_div = """
SELECT un2.Team, un2.[Max Scored Images Category], un2.[Total CCS Score], Division.Division
FROM (SELECT un.Team, Max(un.[Scored Images Category]) AS [Max Scored Images Category], Sum(un.[CCS Score]) AS [Total CCS Score]
FROM (
  SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round1]
  UNION SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round2]
  UNION SELECT [Team], [Scored Images Category], [CCS Score], [Round]
  FROM [Round3]
) AS un
GROUP BY un.Team
HAVING [Max Scored Images Category] = ?
ORDER BY Sum(un.[CCS Score]) DESC
) AS un2
LEFT JOIN Division ON un2.Team = Division.Team;
"""

category_lookup = {1:"Junior",2:"Senior"}

csvfile = open("Totals.csv","w")
csvfile.write("Team ID,Scored Images Category,Total CCS Score,Division\n")
data = DB.run_sql(totals_sql_div)
for i in data:
    csvfile.write("%s,%s,%s,%s\n" % (i[0],category_lookup[i[1]],i[2],i[3]))
csvfile.close()

csvfile = open("JuniorTotals.csv","w")
csvfile.write("Team ID,Scored Images Category,Total CCS Score,Division\n")
data = DB.run_sql(totals_category_sql_div,(1,))
for i in data:
    csvfile.write("%s,%s,%s,%s\n" % (i[0],category_lookup[i[1]],i[2],i[3]))
csvfile.close()

csvfile = open("SeniorTotals.csv","w")
csvfile.write("Team ID,Scored Images Category,Total CCS Score,Division\n")
data = DB.run_sql(totals_category_sql_div,(2,))
for i in data:
    csvfile.write("%s,%s,%s,%s\n" % (i[0],category_lookup[i[1]],i[2],i[3]))
csvfile.close()

print("Closing DB")
DB.exit()
print("Done.")
