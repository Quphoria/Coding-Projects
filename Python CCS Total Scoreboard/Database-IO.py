import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Owner\Desktop\Coding Projects\Access and Python\Test Database.accdb;')
cursor = conn.cursor()
cursor.execute("""
SELECT un.ID, Sum(un.Points) AS TotalPoints
FROM (
  SELECT ID, Points, Round
  FROM Data1
  UNION SELECT ID, Points, Round
  FROM Data2
) AS un
GROUP BY un.ID
ORDER BY Sum(un.Points) DESC;
""")

for row in cursor.fetchall():
    print (row)
