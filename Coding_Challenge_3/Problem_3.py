# 3. Working with CSV
# Using the Atmospheric Carbon Dioxide Dry Air Mole Fractions from quasi-continuous daily measurements at Mauna Loa, Hawaii dataset, obtained from here (https://github.com/datasets/co2-ppm-daily/tree/master/data).
#
# Using Python (csv) calculate the following:
#
# Annual average for each year in the dataset.
# Minimum, maximum and average for the entire dataset.
# Seasonal average if Spring (March, April, May), Summer (June, July, August), Autumn (September, October, November) and Winter (December, January, February).
# Calculate the anomaly for each value in the dataset relative to the mean for the entire time series

import csv

#Create 3 lists that I will use for calculations
year_list, month_list, value_list = [], [], []

with open("co2-ppm-daily.csv") as co2:
    csv_reader = csv.reader(co2, delimiter=',')
    line_count = 0 # I use this for calculating mean later.
    headerline = next(co2) # I use this to skip the header line
    print(headerline)
    for row in csv_reader:
        year, month, day = row[0].split("-") # Here I split my date string into queryable chunks
        if year not in year_list:
            year_list.append(year) # builds a year list
        if month not in month_list:
            month_list.append(month) # builds a month list

        value_list.append(float(row[1])) # this stores my values in a list, you must make this a float or math will fail
        line_count = line_count + 1 # how many datapoints in total.

print("Minimum = " + str(min(value_list)))
print("Maximum = " + str(max(value_list)))
print("Average = " + str(float(sum(value_list) / int(line_count))))
print("Average 2 = " + str(sum(value_list) / len(value_list)))

year_value_dict = {}
for year in year_list:
    temp_year_list = []
    with open ("co2-ppm-daily.csv") as co2:
        csv_reader = csv.reader(co2, delimiter=',')
        headerline = next(co2)

        for row in csv_reader:
            year_co2, month_co2, day = row[0].split("-")
            if year_co2 == year:
                temp_year_list.append(float(row[1]))
    year_value_dict[year] = str(sum(temp_year_list) / len(temp_year_list))

print(year_value_dict)

# Season lists
spring_list = []
summer_list = []
winter_list = []
autumn_list = []

with open ("co2-ppm-daily.csv") as co2:
    csv_reader = csv.reader(co2, delimiter=',')
    headerline = next(co2)

    for row in csv_reader:
        year_co2, month_co2, day = row[0].split("-")
        if month_co2 == '03' or month_co2 == '04' or month_co2 =='05':
            spring_list.append(float(row[1]))
        if month_co2 == '06' or month_co2 == '07' or month_co2 =='08':
            summer_list.append(float(row[1]))
        if month_co2 == '09' or month_co2 == '10' or month_co2 =='11':
            autumn_list.append(float(row[1]))
        if month_co2 == '12' or month_co2 == '01' or month_co2 =='2':
            winter_list.append(float(row[1]))

# Calculating anomoly for each value
Average = sum(value_list) / len(value_list)
value_list_dict = {}

with open("co2-ppm-daily.csv") as co2:
    csv_reader = csv.reader(co2, delimiter=',')
    headerline = next(co2)

    for row in csv_reader:
        year_co2, month_co2, day = row[0].split("-")
        value_list_dict[row[0]] = float(row[1]) - Average
print(value_list_dict)



