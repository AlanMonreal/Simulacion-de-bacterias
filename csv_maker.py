import csv
from time import time as timestamp


def create_csv(data):
    now = timestamp()
    with open("reports/report-" + str(now) + ".csv", 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in data:
            for row in item:
                arr = []
                for it in row:
                    arr.append(it)
                filewriter.writerow(arr)
    print('csv done!')
