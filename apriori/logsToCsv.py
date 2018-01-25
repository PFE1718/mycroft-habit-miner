import hashlib, json, csv
from datetime import datetime, timedelta


hashes = []
tableCsv = []
dateTimeObj0 = datetime.strptime('2018-01-01 00:00:00.0', '%Y-%m-%d %H:%M:%S.%f')

with open ('logsv2.json') as json_data:
    for i,line in enumerate(json_data):
        data = json.loads(line)
        dateTimeObj1 = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        delta = dateTimeObj1 - dateTimeObj0

        del data['datetime']
        hash = hashlib.md5(line).hexdigest()

        if delta > timedelta(minutes=5):
            tableCsv.append(hashes)
            hashes = []
            hashes.append(hash)
            dateTimeObj0 = dateTimeObj1
        else :
            hashes.append(hash)

del tableCsv[0]
for i,line in enumerate(tableCsv):
    print (i+1,line)

with open('inputApriori.csv', 'w') as fp:
    writer = csv.writer(fp, delimiter=',')
    for row in tableCsv:
        writer.writerow(row)