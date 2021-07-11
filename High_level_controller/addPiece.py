

import math
#black 1 white 2 in array
#          1 2 3 4 5 6 7 8 9   
row0 =  [3,3,3,3,3,3,3,3,3,3,3] #
row1 =  [3,1,1,1,1,0,0,0,1,1,3] #9
row2 =  [3,2,1,2,2,0,1,1,2,1,3] #18
row3 =  [3,0,0,0,0,1,0,0,0,0,3] #27
row4 =  [3,0,0,0,0,0,0,0,0,0,3] #36
row5 =  [3,0,0,0,0,0,0,0,0,0,3] #45
row6 =  [3,0,0,0,0,0,0,0,0,0,3] #54
row7 =  [3,0,0,0,0,0,0,0,0,0,3] #63
row8 =  [3,0,0,0,0,0,0,0,0,0,3] #72
row9 =  [3,0,0,0,0,0,0,0,0,0,3] #81
row10 = [3,3,3,3,3,3,3,3,3,3,3]

myList = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]

num_of_pieces = []
locations_of_removed_pieces = []
locations_to_move_back = []
path = [] # at what point in the array it 
x_arr = []
drictions_list = []
path_locations = []
list_path_locations = []
storage = 0
list_locations_of_removed_pieces = []

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
    global locations_of_removed_pieces
    global path
    global x_arr
    global drictions_list
    global path_locations
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

                drictions = str(z)+ " "
                path_coordinates =  ""
                remove_locations = ""

                #first y
                for k in range(len(y_locations_to_check)-j):#how high I should go the first time
                    drictions = drictions + "up "
                    path_coordinates = path_coordinates + str(x_locations_to_check[0]) + "." + str(y_locations_to_check[k]) + " "
                    if(myList[y_locations_to_check[k]][x_locations_to_check[0]] != 0):
                        if (str(y_locations_to_check[k]) + "." + str(x_locations_to_check[0])) != (str(x) + "." + str(y)):
                            num_of_pieces_counter += 1
                            remove_locations = remove_locations + str(x_locations_to_check[0]) + "." + str(y_locations_to_check[k]) + " "
                    p = 1
                
                #first x
                for l in range(len(x_locations_to_check)-i):#how far should I go the first time
                    if (l == 0) and (p == 1):
                        pass
                    else:
                        drictions = drictions + "side "
                        path_coordinates = path_coordinates + str(x_locations_to_check[l]) + "." + str(y_locations_to_check[k]) + " "
                        if(myList[y_locations_to_check[k]][x_locations_to_check[l]] != 0):
                            if (str(y_locations_to_check[k]) + "." + str(x_locations_to_check[l])) != (str(x) + "." + str(y)):
                                num_of_pieces_counter += 1
                                remove_locations = remove_locations + str(x_locations_to_check[l]) + "." + str(y_locations_to_check[k]) + " "

                
                
                #second y
                for m in range(j):#how high should I go the second time
                    drictions = drictions + "up "
                    path_coordinates = path_coordinates + str(x_locations_to_check[l]) + "." + str(y_locations_to_check[k+m+1]) + " "
                    if(myList[y_locations_to_check[k+m+1]][x_locations_to_check[l]] != 0):
                        if (str(y_locations_to_check[k+m+1]) + "." + str(x_locations_to_check[l])) != (str(x) + "." + str(y)):
                            num_of_pieces_counter += 1
                            remove_locations = remove_locations + str(x_locations_to_check[l]) + "." + str(y_locations_to_check[k+m+1]) + " "
  
                #second x
                for n in range(i):#how far should I go the second time

                    drictions = drictions + "side "
                    path_coordinates = path_coordinates + str(x_locations_to_check[l+n+1]) + "." + str(y_locations_to_check[k+m+1]) + " "
                    if(myList[y_locations_to_check[k+m+1]][x_locations_to_check[l+n+1]] != 0):
                        if (str(y_locations_to_check[k+m+1]) + "." + str(x_locations_to_check[l+n+1])) != (str(x) + "." + str(y)):

                            num_of_pieces_counter += 1  
                            remove_locations = remove_locations + str(x_locations_to_check[l+n+1]) + "." + str(y_locations_to_check[k+m+1]) + " "
  

                
                path.append(str(i)+"."+str(j))
                x_arr.append(z)
                num_of_pieces.append(num_of_pieces_counter)
                num_of_pieces_counter = 0
                drictions_list.append(drictions)
                path_locations.append(path_coordinates)
                locations_of_removed_pieces.append(remove_locations)


    #***************************************************************************************************
    #clean up for next time
        x_locations_to_check.clear()
    return

def clean_lists():
    global num_of_pieces
    global path
    global x_arr
    global drictions_list
    global path_locations
    global locations_of_removed_pieces
    global locations_to_move_back
    global list_path_locations

    num_of_pieces.clear()
    path.clear()
    x_arr.clear()
    drictions_list.clear()
    path_locations.clear()
    locations_of_removed_pieces.clear()
    locations_to_move_back.clear()
    list_path_locations.clear()

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
    
def str_to_int_coor(string_location): #takes the location as a string and returns an array loc[x,y]
    float_locations = float(string_location)
    fractional, whole = math.modf(float_locations)
    values = []
    values.append(int(whole))
    values.append(int(fractional * 10.1))
    return(values)

def int_to_string(x,y): #takes x and y and returns "x.y"
    string = str(x) + "." + str(y)
    return(string)

def move_piece_get_ready(px,py):

    global num_of_pieces
    global path
    global x_arr
    global drictions_list
    global myList
    global locations_of_removed_pieces
    global locations_to_move_back
    global list_path_locations
    global list_locations_of_removed_pieces

    x_locations_to_check = []
    y_locations_to_check = []
    pieces_in_way = []
    moves = []

    calculate_paths(px,py)
    #print(len(set(drictions_list)))  #number of unique instructions, not great but not terrible
    best_move_index = find_best_move()

    p_num_of_pieces = num_of_pieces[best_move_index] #number of pieces that are in the way
    p_locations_of_removed_pieces = locations_of_removed_pieces[best_move_index] #locations of the removed pieces from the board
    p_directions_list = drictions_list[best_move_index] #directions for reading
    p_path_locations = path_locations[best_move_index] #locations that the path traverses as string with soace between locations

    p_list_path_locations = p_path_locations.split()
    list_path_locations = p_list_path_locations
    p_list_locations_of_removed_pieces = p_locations_of_removed_pieces.split()
    list_locations_of_removed_pieces = p_list_locations_of_removed_pieces

    #get individual numbers that are needed
    print(p_directions_list)
    print(p_num_of_pieces)
    print(p_path_locations)
    print(p_list_path_locations)
    print(p_list_locations_of_removed_pieces)
    
    # dont need this as the values are already calculated in the path_locations array

        # #recalculate the arrays 

        # #calculate y array
        # for i in range(y):
        #     y_locations_to_check.append(i+1)

        # #calculate all possible x arrays



        # #make array of locations that we want to check
        # if p_x_arr < x:
        #     count = x - p_x_arr + 1
        #     for i in range(count):
        #         x_locations_to_check.append(p_x_arr + i)

        # elif p_x_arr > x:
        #     count = p_x_arr - x + 1
        #     for i in range(count):
        #         x_locations_to_check.append(p_x_arr - i)

        # elif p_x_arr == x: 
        #     x_locations_to_check.append(x)

        # print(x_locations_to_check)
        # print(y_locations_to_check)

    
    #************************************GOT DATA NOW EXECUTE*************************************************************

    # need to remove the pieces in the path
    for location in p_list_locations_of_removed_pieces:
        if location != str(px) + "." + str(py):
            lock = 0 #unlock lock
            coordnates = str_to_int_coor(location)
            x = coordnates[0]
            y = coordnates[1]
            if x > 1:
                if myList[y][x-1] == 0:
                    check = int_to_string(x-1, y)
                    if check not in p_list_path_locations:
                        lock = 1
                        #we are going to move the piece to negative x directoion
                        #print("Move Piece left one")
                        #selector_down()
                        moves.append("z0")
                        #move_x(x)
                        moves.append(['x',x])
                        #print("move_x "+str(x) )
                        #move_y(y)
                        moves.append(['y',y])
                        #print("move_y "+str(y) )
                        #selector_up()
                        moves.append("z1")
                        #move_x(x-1)
                        moves.append(['x',x-1])
                        #print("move_x "+str(x-1) )
                        #selector_down()
                        #moves.append("z0")
                        locations_to_move_back.append(int_to_string(x-1,y))
            if x < 9:
                if myList[y][x+1] == 0:
                    check = int_to_string(x+1, y)
                    if check not in p_list_path_locations:
                        if lock == 0:
                            lock = 1
                            #we are going to move piece to positive x direction
                            #print("move Piece right one")
                            #selector_down()
                            moves.append("z0")
                            #move_x(x)
                            moves.append(['x',x])
                            #print("move_x "+str(x) )
                            #move_y(y)
                            moves.append(['y',y])
                            #print("move_y "+str(y) )
                            #selector_up()
                            moves.append("z1")
                            #move_x(x+1)
                            moves.append(['x',x+1])
                            #print("move_x "+str(x-1) )
                            #selector_down()
                            #moves.append("z0")
                            locations_to_move_back.append(int_to_string(x+1,y))          
            
            if y > 1: 
                if myList[y-1][x] == 0:
                    check = int_to_string(x, y-1)
                    if check not in p_list_path_locations:
                        if lock == 0:
                            lock = 1
                            #move piece -1 in y direction
                            #print("move piece down one")
                            #selector_down()
                            moves.append("z0")
                            #move_x(x)
                            moves.append(['x',x])
                            #print("move_x "+str(x) )
                            #move_y(y)
                            moves.append(['y',y])
                            #print("move_y "+str(y) )
                            #selector_up()
                            moves.append("z1")
                            #move_x(y-1)
                            moves.append(['y',y-1])
                            #print("move_x "+str(x-1) )
                            #selector_down()
                            #moves.append("z0")
                            locations_to_move_back.append(int_to_string(x,y-1))
                            
            if y < 9:
                if myList[y+1][x] == 0:
                    check = int_to_string(x, y+1)
                    if check not in p_list_path_locations:
                        if lock == 0:
                            lock = 1
                            #move piece +1 in y direction 
                            #print("Move a piece up one")
                            #selector_down()
                            moves.append("z0")
                            #move_x(x)
                            moves.append(['x',x])
                            #print("move_x "+str(x) )
                            #move_y(y)
                            moves.append(['y',y])
                            #print("move_y "+str(y) )
                            #selector_up()
                            moves.append("z1")
                            #move_x(y+1)
                            moves.append(['y',y+1])
                            #print("move_y "+str(y+1) )
                            #selector_down()
                            #moves.append("z0")
                            locations_to_move_back.append(int_to_string(x,y+1))
                                    
            if lock == 0:
                count = 0
                for i in p_list_path_locations:
                    count = count + 1
                    if i == location:
                        number = str_to_int_coor(i)
                        x_o = number[0]
                        y_o = number[1]

                        #move one space at a time
                        #print("Need to move Piece off of the board")

                        #Go to location
                        #selector_down()
                        moves.append("z0")

                        #move_x(x)
                        moves.append(['x',x_o])
                        #move_y(y)
                        moves.append(['y',y_o])

                        #selector_up()
                        moves.append("z1")
                        for j in reversed(range(0, count-1)):
                            number = str_to_int_coor(p_list_path_locations[j])
                            x = number[0]
                            y = number[1]

                            #move_x(x)
                            #print("move_x "+str(x))
                            moves.append(['x',x])
                            #move_y(y)
                            #print("move_y "+str(y) )
                            moves.append(['y',y])

                        #Test that did not work.  May go back to later
                            # if j == (count-2):
                            #     #move_x(x)
                            #     #print("move_x "+str(x))
                            #     moves.append(['x',x])
                            #     #move_y(y)
                            #     #print("move_y "+str(y) )
                            #     moves.append(['y',y])
                            # else:
                            #     if moves[-2][1] != x:
                            #         #move_x(x)
                            #         #print("move_x "+str(x))
                            #         moves.append(['x',x])
                            #         if moves[-2][1] != y:
                            #             #move_y(y)
                            #             #print("move_y "+str(y) )
                            #             moves.append(['y',y])
                            #     elif moves[-1][1] != y:
                            #         #move_y(y)
                            #         #print("move_y "+str(y) )
                            #         moves.append(['y',y])

                        #move to empty location off of board
                        #print("Off of the board")
                        locations_to_move_back.append("Off of Board")
                        if myList[y_o][x_o] == 1:
                            moves.append("r1")
                        elif myList[y_o][x_o] == 2:
                            moves.append("r2")

                        #selector_down()
                        #moves.append("z0")
                        #break
            #print("")
    return(moves)

def same_x(i, list_path_locations):
    global storage
    number = str_to_int_coor(list_path_locations[i])
    x1 = number[0]

    try:
        number = str_to_int_coor(list_path_locations[i+1])
    except:
        storage = i
        return(storage)    
    x2 = number[0]
    
    if x1 == x2:
        storage = i
        return(storage)   
    else:
        same_x(i+1,list_path_locations)

def same_y(i,list_path_locations):
    global storage
    number = str_to_int_coor(list_path_locations[i])
    y1 = number[1]

    try:
        number = str_to_int_coor(list_path_locations[i+1])
    except:
        storage = i
        return(storage)
    y2 = number[1]
    
    if y1 == y2:
        storage = i
        return(storage)
    else:
        same_y(i+1,list_path_locations)

def move_piece_onto_board(px,py,colour):
    global list_path_locations
    global myList
    global storage
    moves = []

    y = str_to_int_coor(list_path_locations[0])[1]
    x = str_to_int_coor(list_path_locations[0])[0]
    if colour == 1:
        moves +=["z0","i1","z1", 'd1', ['y', y], ['x', x]]
    elif colour == 2:
        moves +=["z0","i2","z1",'d2', ['y', y], ['x', x]]

    #print("add piece to game board at " + list_path_locations[0])
    # moves.append(["storage at", list_path_locations[0]])

    #get piece from dispenser and put at path_locations[0]
    # selector_up()
    # moves.append("z1")

    start = 0
    same_y(start,list_path_locations)
    cor = str_to_int_coor(list_path_locations[storage])
    y = cor[1]
    #move_y(y)
    moves.append(['y',y])
    #print("move_y "+str(y) )


    same_x(storage,list_path_locations)
    cor = str_to_int_coor(list_path_locations[storage])
    x = cor[0]
    #move_x(x)
    moves.append(['x',x])
    #print("move_x "+str(x) )

    same_y(storage,list_path_locations)
    cor = str_to_int_coor(list_path_locations[storage])
    y = cor[1]
    if y != moves[6][1]:
        #move_y(y)
        moves.append(['y',y])
        #print("move_y "+str(y) )

    same_x(storage,list_path_locations)
    cor = str_to_int_coor(list_path_locations[storage])
    x = cor[0]
    if x != moves[7][1]:
        #move_x(x)
        moves.append(['x',x])
        #print("move_x "+str(x) )

    #selector_down()
    #moves.append("z0")

    #print("")

    myList[py][px] = colour
    return(moves)

def remove_piece_from_board(px,py):

    global list_path_locations
    global myList
    global storage
    moves = []


    reversed_path_locations = list_path_locations[::-1]
    print(reversed_path_locations)
    cor = str_to_int_coor(reversed_path_locations[0])
    x = cor[0]
    y = cor[1]

    #selector_down()
    moves.append("z0")
    #move_x(x)
    moves.append(['x',x])
    #move_y(y)
    moves.append(['y',y])
    #selector_up()
    moves.append("z1")

    start = 0
    same_x(start,reversed_path_locations)
    cor = str_to_int_coor(reversed_path_locations[storage])
    x = cor[0]
    #move_x(x)
    moves.append(['x',x])
    #print("move_x "+str(x) )

    same_y(storage,reversed_path_locations)
    cor = str_to_int_coor(reversed_path_locations[storage])
    y = cor[1]
    #move_y(y)
    moves.append(['y',y])
    #print("move_y "+str(y) )

    same_x(storage,reversed_path_locations)
    cor = str_to_int_coor(reversed_path_locations[storage])
    x = cor[0]
    #move_x(x)
    if x != moves[4][1]:
        moves.append(['x',x])
        #print("move_x "+str(x) )


    same_y(storage,reversed_path_locations)
    cor = str_to_int_coor(reversed_path_locations[storage])
    y = cor[1]
    #move_y(y)
    if y != moves[5][1]:
        moves.append(['y',y])
        #print("move_y "+str(y) )

    #remove piece from board
    if myList[py][px] == 1:
        moves.append("r1")
    elif myList[py][px] == 2:
        moves.append("r2")
    #moves.append("z0")

    myList[py][px] = 0

    return(moves)

def clean_up():
    #print("clean up")
    global locations_to_move_back
    global list_locations_of_removed_pieces
    global list_path_locations
    global myList
    moves = []
     
    reversed_locations_to_move_back = locations_to_move_back[::-1]
    reversed_locations_of_removed_pieces = list_locations_of_removed_pieces[::-1]

    count1 = 0
    for i in reversed_locations_to_move_back:
        if i == "Off of Board":
            colour_value = str_to_int_coor(reversed_locations_of_removed_pieces[count1])
            num = str_to_int_coor(list_path_locations[0])
            x = num[0]
            y = num[1]
            if myList[colour_value[1]][colour_value[0]] == 1:
                moves +=["z0","i1","z1","d1"] #black
            else:
                moves +=["z0","i2","z1","d2"] #white


            #move back onto board
            count2 = 0
            #selector_up()
            for j in list_path_locations:

                num = str_to_int_coor(j)
                x = num[0]
                y = num[1]

                #move_x(x)
                #print("move_x "+str(x) )
                moves.append(['x',x])
                #move_y(y)
                #print("move_y "+str(y))
                moves.append(['y',y])


                count2 = count2 + 1
                if j == reversed_locations_of_removed_pieces[count1]:
                    #moves.append("z0")
                    break
        else:
            num1 = str_to_int_coor(reversed_locations_to_move_back[count1])
            x1 = num1[0]
            y1 = num1[1]

            #selector_down()
            moves.append("z0")
            #move_x(x1)
            moves.append(['x',x1])
            #print("move_x "+str(x1) )
            #move_y(y1)
            moves.append(['y',y1])
            #print("move_y "+str(y1))
            #selector_up()
            moves.append("z1")

            num2 = str_to_int_coor(reversed_locations_of_removed_pieces[count1])
            x2 = num2[0]
            y2 = num2[1]

            #move_x(x2)
            #print("move_x "+str(x2) )
            moves.append(['x',x2])
            #move_y(y2)
            #print("move_y "+str(y2))
            moves.append(['y',y2])
            #selector_down()
            #moves.append("z0")
            
        count1 = count1 + 1
        #print("")
    
    moves.append("z0")
    clean_lists()
    return(moves)

def add_piece_moves_wrapper(px,py,colour):
    moves_final = []

    moves = move_piece_get_ready(px,py)
    moves_final += moves
    moves = move_piece_onto_board(px,py,colour)
    moves_final += moves
    moves = clean_up()
    moves_final += moves
    return(moves_final)

def remove_piece_moves_wrapper(px,py):
    moves_final = []

    moves = move_piece_get_ready(px,py)
    moves_final += moves
    moves = remove_piece_from_board(px,py)
    moves_final += moves
    moves = clean_up()
    moves_final += moves
    return(moves_final)

def add_piece_to_array(px,py,colour):
    global myList

    myList[py][px] = colour


add_piece_to_array(6,1,2)
add_piece_to_array(5,1,2)
add_piece_to_array(7,1,2)
#print(remove_piece_moves_wrapper(6,6))
print(add_piece_moves_wrapper(6,6,1))