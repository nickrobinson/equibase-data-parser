from bs4 import BeautifulSoup
from datetime import datetime
import csv
import boto3
from botocore.client import Config
from io import StringIO

session = boto3.Session(region_name = 'us-east-1', profile_name='minio')
s3 = session.resource('s3',
                    endpoint_url='http://192.168.1.131:9000',
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')

date = datetime.today().strftime('%Y-%m-%d')

obj = s3.Object("equibase", "/{}/stats/horses/LRL/horse_stats.html".format(date))
stats = obj.get()['Body']

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

csv_buffer = StringIO()

writer = csv.writer(csv_buffer)
writer.writerows(output_rows)

s3.Object('equibase', '{}/stats/horses/LRL/stats.csv'.format(date)).put(Body=csv_buffer.getvalue())