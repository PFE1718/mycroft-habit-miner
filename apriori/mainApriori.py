import hashlib, json, csv
from datetime import datetime, timedelta
from apriori import runApriori, dataFromFile


def get_habits(logs_file_path='logs.json', min_supp = 0.06):
    hashes = []
    table_csv = []
    dateTimeObj0 = datetime.strptime('2018-01-01 00:00:00.0', '%Y-%m-%d %H:%M:%S.%f')

    # Open logs and put them in a list, same line if consequent logs are in 5 minutes interval
    with open(logs_file_path) as json_data:
        for i, line in enumerate(json_data):
            data = json.loads(line)
            date_time_obj1 = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S.%f')
            delta = date_time_obj1 - dateTimeObj0

            del data['datetime']
            hash = hashlib.md5(json.dumps(data)).hexdigest()

            if delta > timedelta(minutes=3):
                table_csv.append(hashes)
                hashes = []
                hashes.append(hash)
                dateTimeObj0 = date_time_obj1
            else :
                hashes.append(hash)

    del table_csv[0]

    # Converts logs list to csv so that we can executre apriori algorithm on them
    with open('inputApriori.csv', 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        for row in table_csv:
            writer.writerow(row)

    in_file = dataFromFile('inputApriori.csv')

    intents, rules = runApriori(in_file, min_supp, 0.5)

    habits_hash = []

    # if we notice a group of intents, we add them to the habits
    for item in intents:
        if len(item[0]) > 1:
            habits_hash.append(item[0])

    habits_clear = []
    habit_clear = []

    # hash logs to clear logs
    for habitHash in habits_hash:
        for intent in habitHash:
            with open(logs_file_path) as json_data:
                for line in json_data:
                    data = json.loads(line)
                    del data['datetime']
                    hash = hashlib.md5(json.dumps(data)).hexdigest()
                    if hash == intent:
                        habit_clear.append(json.dumps(data))
                        break
        habits_clear.append(habit_clear)
        habit_clear = []

    return habits_clear