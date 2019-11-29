import csv


def read():
    data = []
    with open('HasilDataBersih.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            data.append(row)

    return data
