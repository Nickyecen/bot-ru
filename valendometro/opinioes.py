import csv
from anytree import Node, RenderTree

#dado um arquivo csv com as comidas e opiniões devolve um menu com as comidas e suas respectivas opiniões
#file = csv file with the food opinions
def get_menu(file):

    # Open the CSV file
    with open(file, newline='') as csvfile:
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

        #Create a tree with all data
        tree = Node("Menu")

        #Iterate over the columns and create a dictionary with the data
        for column in columns[1:]:
            data = {"nome" : (column[0].lower()).split(), "valendometro": float(column[-2]), "polemometro" : float(column[-1])}
            InsertColumn(tree, data)
        
        return tree

#Given a tree and a column, insert the column in the tree
#tree = tree with the data
#data = dictionary with the data for a food
def InsertColumn(tree, data):
    #NODE STRUCTURE
    #.name = key name of the node
    #.valendometro = valendometro of the node
    #.polemometro = polemometro of the node
    #.children = list of children of the node

    #If the data is empty, return
    if len(data["nome"]) == 0:
        return

    Found_before = False

    for child in tree.children:
        #If the node already exists, update the data
        if child.name == data["nome"][0]:
            Found_before = True
            
            #If the data is a son, return
            reconhecidos = len(child.children)
            
            child.valendometro = (child.valendometro * reconhecidos + data["valendometro"]) / (reconhecidos + 1)
            child.polemometro = (child.polemometro * reconhecidos + data["polemometro"]) / (reconhecidos + 1)
            
            #And further update the tree
            new_data = {"nome" : data["nome"][1:], "valendometro" : data["valendometro"], "polemometro" : data["polemometro"]}
            InsertColumn(child, new_data)

    #If the node doesn't exist, create a new one
    if not Found_before:
        new_node = Node(data["nome"][0], parent=tree, valendometro=data["valendometro"], polemometro=data["polemometro"])
        new_data = {"nome" : data["nome"][1:], "valendometro" : data["valendometro"], "polemometro" : data["polemometro"]}
        InsertColumn(new_node, new_data)

    return

#Given a food and a menu, return the valendometro, polemometro
#food = food name.lower().split()
#tree = tree with the food data
def get_food(food, tree, data):
    #If the food is empty, return
    if len(food) == 0:
        return data

    found = False
    
    #Iterate over the children of the tree
    for child in tree.children:
        #If the child is the food, return the data
        if child.name == food[0]:
            found = True
            data["valendometro"] = child.valendometro
            data["polemometro"] = child.polemometro

            return get_food(food[1:], child, data)
        
    #If the food is not found, return an current data
    if not found:
        return data
 
#Given a food and a tree, return the valendometro and polemometro of the food
#food = food name
#tree = tree with the food data
def get_food_opinion(food, tree):
    food_data = food.lower().split()

    return get_food(food_data, tree, {"valendometro" : -1, "polemometro" : -1})

#Given a list of foods and a file, return the valendometro and polemometro of the foods
#foods = list of foods
#file = file with the food opinions
def get_today_opinion(foods, file):
    #Preprocess the data
    foods_data = foods.split("\n")
    tree = get_menu(file)

    #Initialize the variables
    valendometro = 0
    polemometro = 0
    reconhecidos = 0

    #Iterate over the foods and get the opinion
    for food in foods_data:
        food_opinion = get_food_opinion(food, tree)

        if food_opinion["valendometro"] != -1:
            valendometro += food_opinion["valendometro"]
            polemometro += food_opinion["polemometro"]
            reconhecidos += 1

            print(food)

    #Get the average
    valendometro = valendometro / reconhecidos
    polemometro = polemometro / reconhecidos

    return {"valendometro" : valendometro, "polemometro" : polemometro, "reconhecidos" : reconhecidos}