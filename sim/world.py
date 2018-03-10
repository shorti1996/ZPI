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

gen = get_weather_hourly()
print(gen)
print(gen.__next__()["NAME"])

# x = 10
# for i in get_weather_hourly():
#     if x > 0:
#         print(i["DATE"])
#         x = x - 1




