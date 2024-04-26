import csv

# Open the CSV file
with open('Valendometro.csv', newline='') as csvfile:
    # Create a reader
    reader = csv.reader(csvfile)
    # Read the header
    header = next(reader)
    # Initialize an empty list for each column
    columns = [[] for _ in range(len(header))]
    # Append the header to each column
    for i, column_name in enumerate(header):
        columns[i].append(column_name)
    # Iterate over rows and append each value to the corresponding column list
    for row in reader:
        for i, value in enumerate(row):
            columns[i].append(value)

# Create a dictionary with the columns
cardapio = {}

for collum in columns:
    cardapio[collum[0]] = {"valendometro" : collum[-2], "polemometro" : collum[-1]}

print(cardapio)