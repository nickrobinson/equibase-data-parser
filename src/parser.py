from bs4 import BeautifulSoup
from datetime import datetime
import csv

date = datetime.today().strftime('%Y-%m-%d')

stats = open("/storage/data/equibase/{}/LRL/horse_stats.html".format(date))
soup = BeautifulSoup(stats.read())
tables = soup.findAll("table")

output_rows = []

headers = tables[0].findAll('th')
header_row = []
for header in headers:
    header_row.append(header.text)
output_rows.append(header_row)

for table in tables:
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)

result = [x for x in output_rows if x != []]

print(result)

with open('/storage/data/equibase/{}/LRL/stats.csv'.format(date), 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)
