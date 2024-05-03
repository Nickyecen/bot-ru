import csv

#dado um arquivo csv com as comidas e opiniões devolve um menu com as comidas e suas respectivas opiniões
def get_menu(data):

    # Open the CSV file
    with open(data, newline='') as csvfile:
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
    menu = {}

    for collum in columns:
        menu[collum[0]] = {"valendometro" : collum[-2], "polemometro" : collum[-1]}

    return menu

#dado um meno e o cardapio do dia devolve o valendometro e polemometro total
def get_valendometro(menu, cardapio):

    #inicializa os valores
    valendometro = 0
    polemometro = 0

    reconhecidos =  0

    #Processa a string de pratos do dia separando so pratos
    pratos = cardapio.split("\n")

    #Verifica se os pratos do dia estão no menu e calcula o valendometro e polemometro
    for prato in pratos:
        if prato in menu:
            valendometro += float(menu[prato]["valendometro"])
            polemometro += float(menu[prato]["polemometro"])
            reconhecidos += 1

    #Evita divisão por zero
    if reconhecidos == 0:
        return "Nenhum prato reconhecido"
    
    #Faz a media do valendometro e polemometro
    valendometro = round(valendometro/reconhecidos, 1)
    
    #Faz algumas coisas a mais pro polemometro ir de 0-10
    polemometro = round((polemometro/reconhecidos), 1)

    return {"valendometro" : valendometro, "polemometro" : polemometro, "reconhecidos" : reconhecidos}