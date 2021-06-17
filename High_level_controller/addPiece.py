#black 1 white 2 in array
#          1 2 3 4 5 6 7 8 9   
row0 =  [3,3,3,3,3,3,3,3,3,3,3] #
row1 =  [3,0,0,0,1,0,0,0,0,0,3] #9
row2 =  [3,0,1,2,1,0,0,0,0,0,3] #18
row3 =  [3,1,0,0,1,0,0,0,0,0,3] #27
row4 =  [3,0,1,0,2,0,0,0,0,0,3] #36
row5 =  [3,0,0,0,0,0,0,0,0,0,3] #45
row6 =  [3,0,0,0,0,0,0,0,0,0,3] #54
row7 =  [3,0,0,0,0,0,0,0,0,0,3] #63
row8 =  [3,0,0,0,0,0,0,0,0,0,3] #72
row9 =  [3,0,0,0,0,0,0,0,0,0,3] #81
row10 = [3,3,3,3,3,3,3,3,3,3,3]

myList = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]

num_of_pieces = []
path = []
x_arr = []
drictions_list = []

#Plan for the steps to add a piece
#
#1. Calculate the availble paths that we want to evaluate 
#2. Compare the paths to see which has the least pieces on it
#3. if tie pick simplist path
#4. generate the instruction that need to be compleated from this
#   - Move Pieces away
#   - Add Piece
#   _ Move pieces back 


#for step one, calculate available paths

#for loop for all the starting location that we can try
def calculate_paths(x,y):
    global myList
    global num_of_pieces
    global path
    global x_arr
    global drictions_list
    num_of_pieces_counter = 0
    x_locations_to_check = []
    y_locations_to_check = []

    #calculate y array
    for i in range(y):
        y_locations_to_check.append(i+1)
    
    #calculate all possible x arrays
    for starting_location in range(9): 
        #since starts at 0 at one so goes from 1 to 9 
        starting_location = starting_location + 1
        #make array of locations that we want to check
        if starting_location < x:
            count = x - starting_location + 1
            for i in range(count):
                x_locations_to_check.append(starting_location + i)

        elif starting_location > x:
            count = starting_location - x + 1
            for i in range(count):
                x_locations_to_check.append(starting_location - i)

        elif starting_location == x: 
            x_locations_to_check.append(x)

    #****************************************************************************************************
        #Array for all x and y locations is created
        for i in range(len(x_locations_to_check)):  #go through x array
            for j in range(len(y_locations_to_check)): #go through y array
                #set starting location
                k = 0
                l = 0
                m = -1
                n = -1
                p = 0
                z = x_locations_to_check[0]

                drictions = str(z )
                #first y
                for k in range(len(y_locations_to_check)-j):#how high I should go the first time
                    drictions = drictions + "up "
                    if(myList[y_locations_to_check[k]][x_locations_to_check[0]] != 0):
                        num_of_pieces_counter += 1
                    p = 1
                
                #first x
                for l in range(len(x_locations_to_check)-i):#how far should I go the first time
                    if (l == 0) and (p == 1):
                        pass
                    else:
                        drictions = drictions + "side "
                        if(myList[y_locations_to_check[k]][x_locations_to_check[l]] != 0):
                            num_of_pieces_counter += 1
                
                
                #second y
                for m in range(j):#how high should I go the second time
                    drictions = drictions + "up "
                    if(myList[y_locations_to_check[k+m+1]][x_locations_to_check[l]] != 0):
                        num_of_pieces_counter += 1  
                #second x
                for n in range(i):#how far should I go the second time

                    drictions = drictions + "side "
                    if(myList[y_locations_to_check[k+m+1]][x_locations_to_check[l+n+1]] != 0):
                        num_of_pieces_counter += 1    

                
                path.append(str(i)+"."+str(j))
                x_arr.append(z)
                num_of_pieces.append(num_of_pieces_counter)
                num_of_pieces_counter = 0
                drictions_list.append(drictions)

#***************************************************************************************************
#clean up for next time
        x_locations_to_check.clear()
    return


def clean_lists():
    global num_of_pieces
    global path
    global x_arr
    global drictions_list

    num_of_pieces.clear()
    path.clear()
    x_arr.clear()
    drictions_list.clear()


def find_best_move():

    global num_of_pieces
    global drictions_list
    first_wave = []
    length_of_moves_first_wave = []

    min_num_in_path = min(num_of_pieces)
    for i in range(len(num_of_pieces)):
        if num_of_pieces[i] == min_num_in_path:
            first_wave.append(i)

    for j in first_wave:
        length_of_moves_first_wave.append(drictions_list[j].count(' '))
    for j in range(len(first_wave)):
        if length_of_moves_first_wave[j] == min(length_of_moves_first_wave):
            return(first_wave[j])
    






calculate_paths(3,4)
print(len(set(drictions_list)))  #number of unique instructions, not great but not terrible
print(find_best_move())