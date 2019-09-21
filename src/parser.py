from bs4 import BeautifulSoup

stats = open("data/horse_stats.html")
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
