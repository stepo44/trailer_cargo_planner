﻿"""
Program przeznaczony jest do zastosowania w obszarze logistyki i transportu.
Pomaga użytkownikowi zaplanować ułożenie ładunku na standardowej naczepie typu "TIR".
Użytkownik posiada dwie możliwość wprowadzenia danych o ładunku (wymiary paczek, waga):
A. Eksport pliku tekstowego z danymi,
B. Manualne wprowadzenie danych o każdej jednostce ładunku.

Algorytm składa się z łańcucha następujących po sobie procedur, czyli wywoływanych kolejno funkcji.
Łańcuch funkcji dzieli się na trzy części:
1. Wprowadzenie i analiza spójność danych otrzymanych od użytkownika (opcja A lub B).
2. Sortowanie danych.
3. Wyświetlenie wyniku końcowego.




ENGLISH

The program is applicable in the logistics area.
It helps user (transport planner) to draft a cargo placement on standard trailer truck 24t.
User has two options to input cargo data (dimensions, weight):
A. Upload of a text file,
B. Manual data entry of each box.

The algorythm is a set of procedures which are functions, called one after another. The functions flow goes as follow:
1. Entry and data cleaning (user's choice A or B).
2. Data sorting.
3. Output to user.
"""





def user_input_choice():
    # pobiera preferencje użytkownika odnośnie sposobu wprowadzenia danych o paczkach. Dwie opcje do wyboru: plik tekstowy lub ręczne wpisywanie
    # get the user's preference on the data entry of boxes. Two options possible: text file upload or manual entry

    def user_input_choice_condition(userChoice):
        
        if userChoice == "A" or userChoice == "a":
            return form_pattern_display()
                            
        elif userChoice == "B" or userChoice == "b":
            return number_of_boxes_input()

        else:
            userChoice = input("Wybierz prawidłowo jedną z dwóch opcji, wpisując 'A' lub 'B'...")
            return user_input_choice_condition(userChoice)

    userChoice = input("""Wybierz opcję, w jaki sposób chcesz wprowadzić dane o wymiarach twoich paczek:
        1. Export pliku tekstowego z gotowymi danymi - kliknij 'A'.
        2. Manualne wprowadzenie wymiarów i wagi każdej z paczkek - kliknij 'B'\n""")

    user_input_choice_condition(userChoice)



    # 1. Input data cleaning (user's option A/B)
    # 1. Analiza spójności danych wprowadzonych przez użytkownika (opcja A lub B)


    # START: functions flow going after option A chosen by user (text file)
    # START: łańcuch funkcji następujących po wyborze przez użytkownika opcji A (plik tekstowy)


def form_pattern_display():
    # pobiera plik tekstowy wskazany przez użytkownika
    # get a text file from user as input  
        
    dataFile = input("""Podaj nazwę pliku tekstowego z danymi do eksportu. Pamiętaj, aby wymiary paczek w pliku podane były według następującego wzoru:
        Paczka nr 1; długość: ... cm; szerokość: ... cm; wysokość: ... cm; waga ... kg 
        Paczka nr 2; długość: ... cm; szerokość: ... cm; wysokość: ... cm; waga ... kg
        Paczka nr 3; długość: ... cm; szerokość: ... cm; wysokość: ... cm; waga ... kg
        itd...\n""")
        
    return count_lines_in_file(dataFile)


def count_lines_in_file(dataFile):
    # liczy ilość wierszy w pliku tekstowym i na tej podstawie podaje ilość paczek do dalszego sortowania (1 wiersz = 1 paczka)
    # count a number of lines in the text file, then get the number of boxes (1 line = 1 box)
        
    numLines = 0
    try:
        data = open(dataFile, 'r')
    except OSError:  # FileNotFoundError is a subclass of OSError
        dataFile = input('\nPlik, o podanej nazwie, nie został odnaleziony. Wprowadź prawidłową nazwę: "data.txt"\n')
        count_lines_in_file(dataFile)

    try:      
        for line in data:
            numLines += 1
    except UnboundLocalError:
        pass
        
    else: return request_for_sorting_nr_a(dataFile, int(numLines))


def request_for_sorting_nr_a(dataFile, numLines):
    # informuje użytownika, że plik został prawidłowo zapisany i jest gotowy do rozpoczęcia sortowania
    # inform user that the file has been succefully uploaded and is ready to start sorting
        
    input("\nTwój plik został prawidłowo wyeksportowany. Kliknij ENTER, aby uruchomić sortowanie paczek.")  
    return create_dicts_for_boxes_from_file(dataFile, numLines)


def create_dicts_for_boxes_from_file(dataFile, numLines):
    # dla każdej z paczek tworzy słownik zawierający klucze dla: nr paczki, jej wymiarów i wagi
    # create an empty dic for each box, containing keys for: the box number, its dimensions and weight

    allBoxesFromFile = []
    for line in range(0, numLines):
        box = {'boxNumber': '', 'length': '', 'width': '', 'height': '', 'weight': ''}
        allBoxesFromFile.append(box)
                    
    return put_boxes_from_file_into_list_of_dicts(allBoxesFromFile, dataFile)

   
def put_boxes_from_file_into_list_of_dicts(allBoxesFromFile, dataFile):
    # odczytuje dane paczek (nr paczki, wymiary, wagę) i kopiuje je do utworzonych, pustych słowników
    # read boxes data (nr of box, dimensions, weight) from the file and put it into the created empty dics

    file = open(dataFile, 'r')
    lineCounter = 0
            
    for eachLine in file:
        try:
            (boxNumber, length, width, height, weight) = eachLine.split(';')
        except ValueError:
            input("\nUps...coś poszło nie tak z odczytywaniem danych. Upewnij się, że dane każdej z paczek zaczynają się od nowego akapitu, a ich poszczególne wymiary oddzielone są od siebie średnikami \";\".\nNastępnie ponownie podaj nazwę pliku. \n")
            return count_lines_in_file(dataFile)

        eachLineList = []
        eachLineList.append(boxNumber)
        eachLineList.append(length)
        eachLineList.append(width)
        eachLineList.append(height)
        eachLineList.append(weight)

        for eachString in eachLineList:

            eachStringList = []
                            
            for letter in str(eachString):

                if letter.isdigit():
                    eachStringList.append(letter)

            cleanStringDimension = int((''.join(eachStringList)))

            try:                
                if eachLineList.index(eachString) == 0:         
                    allBoxesFromFile[lineCounter]['boxNumber']=cleanStringDimension

                elif eachLineList.index(eachString) == 1:         
                    allBoxesFromFile[lineCounter]['length']=cleanStringDimension

                elif eachLineList.index(eachString) == 2:
                    allBoxesFromFile[lineCounter]['width']=cleanStringDimension
                                                        
                elif eachLineList.index(eachString) == 3:         
                    allBoxesFromFile[lineCounter]['height']=cleanStringDimension

                elif eachLineList.index(eachString) == 4:         
                    allBoxesFromFile[lineCounter]['weight']=cleanStringDimension

            except IndexError:
                pass

            del eachStringList, cleanStringDimension
                            
        lineCounter += 1

    return check_total_weight_limit_from_exported_file(allBoxesFromFile)


def check_total_weight_limit_from_exported_file(allBoxesFromFile):
    # sprawdza dopuszczalny limit wagowy na naczepie (max 24000kg); sumuje wagi wszystkich paczek
    # check the weight limit (24000kg max allowed on a trailer) by adding weights of all boxes

    totalWeight = sum([box['weight'] for box in allBoxesFromFile])

    if totalWeight > 24000:
        weightSurplus = totalWeight - 24000
        input("\nŁączna waga twoich paczek przekracza dopuszczalną ładowność ciężarówki, która wynosi max. 24 tony. Naczepa przeładowana jest o {} kg. Usuń część paczek i spróbuj jeszcze raz.\n".format(weightSurplus))
        return user_input_choice()
            
    else: separate_garbage(allBoxesFromFile)


# END: functions flow of the option A (text file)
# KONIEC: łańcucha funkcji następujących po wyborze opcji A (plik tekstowy)





# START: functions flow of the option B chosen by user (manual data entry)
# START: łańcuch funkcji następujących po wyborze przez użytownika opcji B (ręczne wprowadzenie danych)


def number_of_boxes_input():
    # prosi użytkownika o wprowadzenie ilości paczek
    # ask user to type a number of boxex

    try:
        numberOfBoxes = int(input("Podaj ilość paczek do załadowania: "))
    except ValueError:
        print("\nPodana wartość jest nieprawidłowa. Używaj tylko pełnych cyfr.")
        return number_of_boxes_input()
    else:    
        if numberOfBoxes <= 0:
            print("\nUps...podałeś {}. To chyba literówka? Popraw się!".format(numberOfBoxes))
            return number_of_boxes_input()
                
        elif 0 < numberOfBoxes < 3:
            print("\nMasz za mało paczek, aby je sortować. To za łatwe dla mnie!:p Wróć jak będziesz miał ich trochę więcej...:)")  
            return number_of_boxes_input()
                
        elif numberOfBoxes > 100:
            print("\nTrochę przesadziłeś...Miej litość i zmniejsz ilość chociaż do 100 sztuk. Merci:)")
            return number_of_boxes_input()
            
        else: return input_data_processing(numberOfBoxes)

            
def input_data_processing(numberOfBoxes):
    # definiuje 4 funkcje pobierające dane odnośnie każdej paczki od użytkownika, odpowiednio: dł., szer., wys., waga
    #   iteruje na każdej z paczek:
    #       - iworzy słownik dla każdej paczki
    #       - pobiera dane odnośnie każdej paczki od użytkownika i umieszcza je w utworzonym słowniku
    #   umieszcza wszystkie słowniki w jednej liście

    # define 4 functions that get user input for each box, respectively, about: length, width, height, weight
    #   loop over boxes:
    #       - create a dic for each box
    #       - get the input data for each box and put it into a dic
    #   put all the created dics into one list

    entryBoxes = []
    # length:
    # długość:    
    def entry_length_clear(length):
            
        try:
            length = int(length)
            if length < 0:
                raise ValueError(print("Długość nie może mieć watości ujemnej."))
        except ValueError:
            length = input("Podaj długość w formie pełnych cyfr bez wartości dziesiętnych...")    
            return entry_length_clear(length)
        else:
            if length > 400:
                length = input("Długość paczki jest za duża, max. 400 cm. Przepakuj i wprowadź ponownie: ")
                return entry_length_clear(length)

            elif length < 50:
                length = input("Długość paczki jest za mała, min. 50 cm. Przepakuj i wprowadź ponownie: ")
                return entry_length_clear(length)
                 
            lengthClear = length
            return length
    # width:
    # szerokość:
    def entry_width_clear(width):
            
        try:
            width = int(width)
            if width < 0:
                raise ValueError(print("Szerokość nie może mieć watości ujemnej."))
        except ValueError:
            width = input("Podaj szerokość w formie pełnych cyfr bez wartości dziesiętnych...")    
            return entry_width_clear(width)
        else:   
            if width > 240:
                width = input("Szerokość paczki jest za duża, max 240 cm. Przepakuj i wprowadź ponownie: ")
                return entry_width_clear(width)

            elif width < 50:
                width = input("Szerokość paczki jest za mała, min. 50 cm. Przepakuj i wprowadź ponownie: ")
                return entry_width_clear(width)

            widthClear = width 
            return widthClear
    # height:
    # wysokość:
    def entry_height_clear(height):
            
        try:
            height = int(height)
            if height < 0:
                raise ValueError(print("Wysokość nie może mieć wartości ujemnej."))
        except ValueError:
            height = input("Podaj wysokość w formie pełnych cyfr bez wartości dziesiętnych...")    
            return entry_height_clear(height)
        else:    
            if height > 260:
                height = input("Wysokość paczki jest za duża, max 260 cm. Przepakuj i wprowadź ponownie: ")
                return entry_height_clear(height)

            height = int(height)
            if height < 50:
                height = input("Wysokość paczki jest za mała, min. 50 cm. Przepakuj i wprowadź ponownie: ")
                return entry_height_clear(height)

            heightClear = height
            return heightClear
    # weight:
    # waga:
    def entry_weight_clear(weight):
            
        try:
            weight = int(weight)
            if weight < 0:
                raise ValueError(print("Waga nie może mieć watości ujemnej."))
        except:
            weight = input("Podaj wagę w formie pełnych cyfr bez wartości dziesiętnych...")
            return entry_weight_clear(weight)
        else:    
            if weight > 24000:
                weight = input("Waga paczki jest za duża. Przepakuj i wprowadź ponownie: ")
                return entry_weight_clear(weight)

            weightClear = weight 
            return weightClear

    for box in range(1, int(numberOfBoxes)+1):
        # pobiera dane od użytkownika i umieszcza je w słownikach
        # get input from user and put it into dicts
            
        length = input("\nPodaj długość {} paczki (cm): ".format(str(box)))
        lengthClear = entry_length_clear(length)
                 
        width = input("Podaj szerokość {} paczki (cm): ".format(str(box)))
        widthClear = entry_width_clear(width)
            
        height = input("Podaj wysokość " + str(box) + " paczki (cm): ")
        heightClear = entry_height_clear(height)
            
        weight = input("Podaj wagę {} paczki (kg): ".format(str(box)))
        weightClear = entry_weight_clear(weight)
            
        dic = {'length': '', 'width': '', 'height': '', 'weight': ''}
        dic['length'] = lengthClear
        dic['width'] = widthClear
        dic['height'] = heightClear
        dic['weight'] = weightClear
            
        entryBoxes.append(dic)

    return check_total_weight_limit_from_manual_entry(entryBoxes)


def check_total_weight_limit_from_manual_entry(entryBoxes):
    # sprawdza dopuszczalny limit wagowy na naczepie (max 24000kg); sumuje wagi wszystkich paczek
    # check the weight limit (24000kg max allowed on a trailer) by adding weights of all boxes

    totalWeight = sum([box['weight'] for box in entryBoxes])

    if totalWeight > 24000:
        weighSurplus = totalWeight - 24000
        input("\nŁączna waga twoich paczek przekracza dopuszczalną ładowność ciężarówki, która wynosi max. 24 tony. Naczepa przeładowana jest o {} kg. Usuń część paczek i spróbuj jeszcze raz.\n".format(weighSurplus))
        return user_input_choice()
            
    else: request_for_sorting_nr_b(entryBoxes)


def request_for_sorting_nr_b(entryBoxes):
    input("\nPaczki zostały wprowadzone. Kliknij ENTER, aby uruchomić sortowanie...\n")
    return separate_garbage(entryBoxes)


# END: functions flow of the option B chosen by user (manual data entry)
# KONIEC: łańcuch funckji następujących po wyborze przez użytownika opcji B (ręczne wprowadzenie danych)




# START: 2. Data sorting
# START: 2. Sortowanie danych


def separate_garbage(allBoxes):
    # wyklucza paczki z anomaliami wymiarowymi z dalszego sortowania. Przechowuje paczki z anomaliami w 'garbageBoxes'
    # exclude boxes with anomalies in dimensions from the further sorting. Store the anomaly boxes in 'garbageBoxes'
        
    garbageBoxes = [box for box in allBoxes if box['width'] < 50 or box['width'] > 240 or box['length'] < 50 or box['length'] > 400 or box['height'] < 50 or box['height'] > 260]
    toSortBoxes = []

    for box in allBoxes:
        if box not in garbageBoxes:
            toSortBoxes.append(box)

    return sort_width(allBoxes, garbageBoxes, toSortBoxes)

        
def sort_width(allBoxes, garbageBoxes, toSortBoxes):
    # grupuje paczki według ich szerokości i umieszcza w 4 sekcjach wymiarowych. Każda sekcja jest listą składającą się ze słowników. Każdy słownik to paczka
    # group boxes according to their width and put them into 4 dimensional sections. Each section is a list of dics. Each dic is a box
        
    bigsRaw = []
    equalsRaw = []
    middlesRaw = []
    smallsRaw = []
        
    for box in toSortBoxes:
        if 241 > box['width'] > 125:
            bigsRaw.append(box)
        elif 110 <= box['width'] <= 125:
            equalsRaw.append(box)
        elif 80 <= box['width'] < 110:
            middlesRaw.append(box)
        elif 50 <= box['width'] < 80:
            smallsRaw.append(box)
                        
    return sort_to_ascending_order(allBoxes, bigsRaw, equalsRaw, middlesRaw, smallsRaw, garbageBoxes)


def sort_to_ascending_order(allBoxes, bigsRaw, equalsRaw, middlesRaw, smallsRaw, garbageBoxes):
    # sortuje wszystkie grupy paczek wg. szer. w porządku rosnącym
    # sort all the width groups in the ascending order
        
    sortWithLength = lambda x: x['length']
        
    bigsOrdered = sorted(bigsRaw, key=sortWithLength)
    equalsOrdered = sorted(equalsRaw, key=sortWithLength)
    middlesOrdered = sorted(middlesRaw, key=sortWithLength)
    smallsOrdered = sorted(smallsRaw, key=sortWithLength)
            
    return sort_equals_length(allBoxes, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes)


def sort_equals_length(allBoxes, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes):
    # w liście equalsOrdered układa paczki w pary wg. ich długości z tolerancją do 60 cm, usuwa sparowane paczki z equalsOrdered, następnie zwraca je w nowej liście: equalsSorted
    # put boxes in pairs within the equalsOrdered list by their length with the tolerance of 60 cm, remove the paired boxes from the equalsOrdered, then return them in a new list: equalsSorted
        
    equalsSorted = []

    def pop_and_append_equals():
     
        if len(equalsOrdered) > 2 and equalsOrdered[1]['length'] - equalsOrdered[0]['length'] < 60:

            thisEqual = equalsOrdered[0]
            thisEqual = equalsOrdered.index(thisEqual)

            elem1InPair = equalsOrdered.pop(thisEqual)
            elem2InPair = equalsOrdered.pop(thisEqual)
            equalsSorted.append(elem1InPair)
            equalsSorted.append(elem2InPair)

            return pop_and_append_equals()
                    
        elif len(equalsOrdered) > 2 and equalsOrdered[2]['length'] - equalsOrdered[1]['length'] < 60:                       

            thisEqual = equalsOrdered[1]
            thisEqual = equalsOrdered.index(thisEqual)
                                           
            elem1InPair = equalsOrdered.pop(thisEqual)
            elem2InPair = equalsOrdered.pop(thisEqual)
            equalsSorted.append(elem1InPair)
            equalsSorted.append(elem2InPair)
     
            return pop_and_append_equals()
                    
        elif len(equalsOrdered) == 2 and equalsOrdered[1]['length'] - equalsOrdered[0]['length'] < 60:

            thisEqual = equalsOrdered[0]
            thisEqual = equalsOrdered.index(thisEqual)

            elem1InPair = equalsOrdered.pop(thisEqual)
            elem2InPair = equalsOrdered.pop(thisEqual)
            equalsSorted.append(elem1InPair)
            equalsSorted.append(elem2InPair)
      
            return pop_and_append_equals()   

        else:
            return compare_bigs_to_middles_length(allBoxes, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes)   
                    
    return pop_and_append_equals()


def compare_bigs_to_middles_length(allBoxes, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes):
    # układa paczki w pary z list: bigsOrdered i middlesOrdered, wg. ich długości z tolerancją do 100 cm. Usuwa sparowane paczki z list: bigsOrdered i middlesOrdered, następnie zwraca je w nowej liście: bigsWithMiddlesSorted
    # put boxes in pairs from the bigsOrdered and middlesOrdered lists by their length with the tolerance of 100 cm. Remove the paired boxes from the bigsOrdered and middlesOrdered lists, then return them in a new list: bigsWithMiddlesSorted
        
    sortWithWidth = lambda y: y['width']
    bigsOrdered = sorted(bigsOrdered, key=sortWithWidth, reverse=True)
    middlesOrdered = sorted(middlesOrdered, key=sortWithWidth, reverse=True)
            
    bigsWithMiddlesSorted = []
            
    if len(bigsOrdered) >= 2 and len(middlesOrdered) >= 2:
                
        for big in bigsOrdered:
            bigIndex = bigsOrdered.index(big)
                        
            for middle in middlesOrdered:
                if big['width'] + middle['width'] <=240 and big['length'] - middle['length'] <=100 and middle['length'] - big['length'] <= 100: # 100 to adjust??

                    middleIndex = middlesOrdered.index(middle)
                    elem2InPair = middlesOrdered.pop(middleIndex)
                    bigsWithMiddlesSorted.append(elem2InPair)
                                        
                    elem1InPair = bigsOrdered.pop(bigIndex)                
                    bigsWithMiddlesSorted.append(elem1InPair)
                
    return compare_bigs_to_smalls_length(allBoxes, bigsWithMiddlesSorted, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes)                    


def compare_bigs_to_smalls_length(allBoxes, bigsWithMiddlesSorted, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes):
    # układa paczki w pary z list: bigsOrdered i smallsOrdered, wg. ich długości z tolerancją do 100 cm. Usuwa sparowane paczki z list: bigsOrdered i smallsOrdered, następnie zwraca je w nowej liście: bigsWithSmallsSorted
    # put boxes in pairs from the bigsOrdered and smallsOrdered lists by their length with the tolerance of 100 cm. Remove the paired boxes from the bigsOrdered and smallsOrdered lists, then return them in a new list: bigsWithSmallsSorted

    sortWithWidth = lambda y: y['width']
    bigsOrdered = sorted(bigsOrdered, key=sortWithWidth, reverse=True)
    smallsOrdered = sorted(smallsOrdered, key=sortWithWidth, reverse=True)
            
    bigsWithSmallsSorted = []
            
    if len(bigsOrdered) >= 2 and len(smallsOrdered) >= 2:
                
        for big in bigsOrdered:
            bigIndex = bigsOrdered.index(big)
                        
            for small in smallsOrdered:
                if big['width'] + small['width'] <=240 and big['length'] - small['length'] <=100 and small['length'] - big['length'] <= 100: # 100 to adjust

                    smallIndex = smallsOrdered.index(small)
                    elem2InPair = smallsOrdered.pop(smallIndex)
                    bigsWithSmallsSorted.append(elem2InPair)
                                        
                    elem1InPair = bigsOrdered.pop(bigIndex)                
                    bigsWithSmallsSorted.append(elem1InPair)

    return compare_equals_to_middles_length(allBoxes, bigsWithSmallsSorted, bigsWithMiddlesSorted, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes)      


def compare_equals_to_middles_length(allBoxes, bigsWithMiddlesSorted, bigsWithSmallsSorted, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes):
    # układa paczki w pary z list: equalsOrdered i middlesOrdered, wg. ich długości z tolerancją do 100 cm. Usuwa sparowane paczki z list: equalsOrdered i middlesOrdered, następnie zwraca je w nowej liście: equalsWithMiddlesSortedLength
    # put boxes in pairs from the equalsOrdered and middlesOrdered lists by their length with the tolerance of 100 cm. Remove the paired boxes from the equalsOrdered and middlesOrdered lists, then return them in a new list: equalsWithMiddlesSortedLength

    sortWithWidth = lambda y: y['width']
    equalsOrdered = sorted(equalsOrdered, key=sortWithWidth, reverse=True)
    middlesOrdered = sorted(middlesOrdered, key=sortWithWidth, reverse=True)

    equalsWithMiddlesSortedLength = []
            
    if len(equalsOrdered) >= 2 and len(middlesOrdered) >= 2:
                
        for equal in equalsOrdered:
            equalIndex = equalsOrdered.index(equal)
                    
            for middle in middlesOrdered:
                    
                if equal['width'] + middle['width'] <=240 and equal['length'] - middle['length'] <=100 and middle['length'] - equal['length'] <= 100:

                    middleIndex = middlesOrdered.index(middle)
                    elem2InPair = middlesOrdered.pop(middleIndex)
                    equalsWithMiddlesSortedLength.append(elem2InPair)

                    elem1InPair = equalsOrdered.pop(equalIndex)                
                    equalsWithMiddlesSortedLength.append(elem1InPair)
                                                    
    return compare_equals_to_smalls_length(allBoxes, bigsWithMiddlesSorted, bigsWithSmallsSorted, equalsWithMiddlesSortedLength, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes) 
                

def compare_equals_to_smalls_length(allBoxes, bigsWithMiddlesSorted, bigsWithSmallsSorted, equalsWithMiddlesSortedLength, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes):
    # put boxes in pairs from the equalsOrdered and smallsOrdered lists by their length with the tolerance of 100 cm. Remove the paired boxes from the equalsOrdered and smallsOrdered lists, then return them in a new list: equalsWithSmallsSortedLength
    # układa paczki w pary z list: equalsOrdered i smallsOrdered, wg. ich długości z tolerancją do 100 cm. Usuwa sparowane paczki z list: equalsOrdered i smallsOrdered, następnie zwraca je w nowej liście: equalsWithSmallsSortedLength

    sortWithLength = lambda x: x['length']
    equalsOrdered = sorted(equalsOrdered, key=sortWithLength, reverse=True)
    equalsWithSmallsSortedLength = []
            
    if len(equalsOrdered) >= 2 and len(smallsOrdered) >= 2:
                
        for equal in equalsOrdered:
            equalIndex = equalsOrdered.index(equal)
                        
            for small in smallsOrdered:
                if equal['length'] - small['length'] <=100 and small['length'] - equal['length'] <= 100:

                    smallIndex = smallsOrdered.index(small)
                    elem2InPair = smallsOrdered.pop(smallIndex)
                    equalsWithSmallsSortedLength.append(elem2InPair)
                                        
                    elem1InPair = equalsOrdered.pop(equalIndex)                
                    equalsWithSmallsSortedLength.append(elem1InPair)
                        
    return create_all_sorted_lists(allBoxes, bigsWithMiddlesSorted, bigsWithSmallsSorted, equalsWithMiddlesSortedLength, equalsWithSmallsSortedLength, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes)                    


def create_all_sorted_lists(allBoxes, bigsWithMiddlesSorted, bigsWithSmallsSorted, equalsWithMiddlesSortedLength, equalsWithSmallsSortedLength, equalsSorted, bigsOrdered, equalsOrdered, middlesOrdered, smallsOrdered, garbageBoxes):
    # scala wszystkie utworzone listy w jedną listę: allSortedLists
    # put together all the created lists into one list: allSortedLists
       
    allSortedLists = []
            
    allSortedLists.append(bigsWithMiddlesSorted)
    allSortedLists.append(bigsWithSmallsSorted)
    allSortedLists.append(equalsWithMiddlesSortedLength)
    allSortedLists.append(equalsWithSmallsSortedLength)
    allSortedLists.append(equalsSorted)
    allSortedLists.append(bigsOrdered)
    allSortedLists.append(equalsOrdered)
    allSortedLists.append(middlesOrdered)
    allSortedLists.append(smallsOrdered)

    return create_all_sorted_boxes(allBoxes, allSortedLists, garbageBoxes)
            

def create_all_sorted_boxes(allBoxes, allSortedLists, garbageBoxes):
    # tworzy nową listę: allSortedBoxes, następnie umieszcza w niej wszystkie paczki z list umieszczonych w allSortedLists
    # create a new list: allSortedBoxes and put into it all the boxes from all the lists of the allSortedLists
         
    allSortedBoxes = []

    for eachList in allSortedLists:
        for eachBox in eachList:
            allSortedBoxes.append(eachBox)

    return create_output(allBoxes, allSortedBoxes, garbageBoxes)


# END: boxes sorting
# KONIEC: sortowanie paczek




# START: 3. Output to user
# START: 3. Wyświetlenie wyniku końcowego


def create_output(allBoxes, allSortedBoxes, garbageBoxes):
    # tworzy output string dla każdej z paczek i umieszcza je w liście: allSortedBoxesString
    # create output strings for each of boxes and put them into a list: allSortedBoxesString

    allSortedBoxesString = []
        
    for sortedBox in allSortedBoxes:
        for box in allBoxes:
            if sortedBox == box:
                boxNumber = str(allBoxes.index(box)+1)
                sortedBoxString = "paczka nr {} o wymiarach: {}(szer) x {}(dł) x {}(wys)".format(boxNumber, str(sortedBox['length']), str(sortedBox['width']), str(sortedBox['height']))
                allSortedBoxesString.append(sortedBoxString)
                                    
    return print_output(allBoxes, allSortedBoxesString, garbageBoxes)


def garbage_output(allBoxes, garbageBoxes):
    # tworzy output string dla każdej z paczek i umieszcza je w liście: allSortedBoxesString
    # create output strings for each of boxes in the garbageBoxes and put them into a list: garbageBoxesString
        
    garbageBoxesString = []
    for garbageBox in garbageBoxes:
        for box in allBoxes:
            if garbageBox == box:
                boxNumber = str(allBoxes.index(box)+1)
                garbageBoxeString = "paczka nr {} o wymiarach: {}(dł) x {}(szer) x {}(wys)".format(boxNumber, str(garbageBox['length']), str(garbageBox['width']), str(garbageBox['height'])) 
                garbageBoxesString.append(garbageBoxeString)

    for garbageString in garbageBoxesString:
        print(garbageString)

    print("""\n\nPamiętaj!. Wymiary naczepy w ciężarówce typu 'plandeka standard', zwanej potocznie 'TIR-em', to: 13,4(dł), 2,45(szer) i 2,8(wys) metra.

    Twoje paczki muszą mieścić się w następujących limitach:
        DŁUGOŚĆ: nie mniejsza niż 50 i nie większa niż 400 cm,
        SZEROKOŚĆ: nie mniejsza niż 50 i nie większa niż 240 cm,
        WYSOKOŚĆ: nie większa niż 260 cm,
        ŁĄCZNA WAGA PACZEK: nie większa niż 24 tony.\n""")

    
def print_output(allBoxes, allSortedBoxesString, garbageBoxes):
    # tworzy końcowy output do użytkownika: print dane z allSortedBoxesString i garbageBoxesString
    # create the final output to user: print data from the allSortedBoxesString and the garbageBoxesString

    for boxString in allSortedBoxesString:
        boxIndex = allSortedBoxesString.index(boxString)
        if boxIndex < len(allSortedBoxesString) - 1:
            if boxIndex == 0:
                print("\n\n      SORTOWANIE ZAKOŃCZONE \n\nUłóż paczki względem ich szerokości w następujących parach:","\n\n", boxString, " i ", allSortedBoxesString[allSortedBoxesString.index(boxString)+1])
            elif boxIndex % 2 == 0:
                print(boxString, " i ", allSortedBoxesString[allSortedBoxesString.index(boxString)+1])

    if len(garbageBoxes) == 0:
        try:
            print("Bez pary, luzem, pozostała {} \n".format(allSortedBoxesString[len(allSortedBoxesString)-1]))
        except IndexError:
            pass
    else:
        try:
            print("Bez pary, luzem, została {}.\n\nNiezaplanowane zostały również paczki z wymiarami, które były zbyt małe lub zbyt duże, aby móc załadować je na ciężarówkę:".format(allSortedBoxesString[len(allSortedBoxesString)-1]))
            garbage_output(allBoxes, garbageBoxes)
        except IndexError:
            pass
                
    reload = input("\nKliknij ENTER, jeśli chcesz wprowadzić nowy zestaw paczek \n")
    print("\n\n\n\n      <<< ROZPOCZYNAMY NOWE SORTOWANIE >>>\n")

    return user_input_choice() 



































































