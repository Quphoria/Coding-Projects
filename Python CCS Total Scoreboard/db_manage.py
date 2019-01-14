# sql1 = '''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)'''

# Larger example that inserts many records at a time
# purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#              ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
#              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
#             ]
# c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

totals_sql = """
SELECT un.ID, Sum(un.Points) AS TotalPoints
FROM (
  SELECT ID, Points, Round
  FROM Data1
  UNION SELECT ID, Points, Round
  FROM Data2
) AS un
GROUP BY un.ID
ORDER BY Sum(un.Points) DESC;
"""

import sqlitedb_IO
DB = sqlitedb_IO.DB()
DB.load()
# DB.run_sql(sql1)
DB.run_sql(sql2)
# DB.save()
for i in DB.run_sql("SELECT * FROM stocks;"):
    print(i)
DB.exit()
