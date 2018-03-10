import csv


def get_weather_hourly():
    with open('weather_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append(row)
            yield row
        # for row in data:
        #     print(row['STATION'], row['DATE'])


def yielder(arg):
    z = 0
    for x in arg:
        z = z + 1
        print("z= " + str(z))
        yield 2 * x


for i in yielder(range(10)):
    print(i)




