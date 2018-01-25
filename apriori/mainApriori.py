import hashlib, json, csv
from datetime import datetime, timedelta
from apriori import runApriori, dataFromFile


def get_habits(logs_file_path='logs.json', min_supp = 0.01, min_confidence = 0.8):
    hashes_temp = []
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

            if delta > timedelta(minutes=5):
                table_csv.append(hashes_temp)
                hashes_temp = []
                hashes_temp.append(hash)
                dateTimeObj0 = date_time_obj1
            else :
                hashes_temp.append(hash)

    del table_csv[0]

    # Converts logs list to csv so that we can executre apriori algorithm on them
    with open('inputApriori.csv', 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        for row in table_csv:
            writer.writerow(row)

    in_file = dataFromFile('inputApriori.csv')

    intents, rules = runApriori(in_file, min_supp, min_confidence)

    # modify a bit the rules and sort the tuples in it
    hashes_temp = []
    for rule in rules:
        hash = rule[0][0] + rule[0][1]
        hashes_temp.append(sorted(hash))

    # this is to remove duplicates
    hashes = []
    for tuple in hashes_temp:
        if tuple not in hashes:
            hashes.append(tuple)


    habits = []
    habit = []
    for hash in hashes:
        for intent in hash:
            with open(logs_file_path) as json_data:
                for line in json_data:
                    data = json.loads(line)
                    del data['datetime']
                    hash = hashlib.md5(json.dumps(data)).hexdigest()
                    if hash == intent:
                        habit.append(json.dumps(data))
                        break
        habits.append(habit)
        habit = []

    # for habit in habits:
    #     for intent in habit:
    #         intent = json.loads(intent)['utterance']
    #         del intent['utterance']

    for line in habits:
        print (line)

get_habits()
