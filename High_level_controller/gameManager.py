import logging
import time

class GameManager:
    def __init__(self):
        self.__mycolour = "Blac"
        self.__turn = 1
        self.__white_score = 0
        self.__black_score = 0
        self.__curent_storage = 1
    
    def __sendPiece(self, pieceAdded):
        self.__socket.connect()
        self.__socket.send_data(bytes(pieceAdded, "utf-8"))
        logging.info("[main]To server: " + str(pieceAdded))

        logging.info("[main]waiting for a new piece from remote player")
        self.__receMesg()

    def __receMesg(self):
        data = self.__socket.read_data()
        mesg = data.decode("utf-8")
        logging.info("[main]From server: " + mesg)
        self.__socket.close_socket()

        for i in range(0, len(mesg), 4):
            code = mesg[i:i+4]
            if(code[0] == "A"):
                # convert web coordinate to physical coordinate
                x = 10 - int(code[3])
                y = 10 - int(code[1])
                #add a Piece to the board in the location of x.y the next three chars in string
                #***********************************************************************************
                #add_piece_to_gameboard(x,y)
                
                # set the piece coordinate in the piece locator, otherwise it considers it is a new piece from the local player
                self.__pl.setCoordinate(x, y)

                # wait until the xy system not busy
                while self.__xy.isBusy():
                    pass
                self.__xy.executeCmd(["z1", ['d', self.__curent_storage], ['y', y], ['x', x], "z0", ['x', 9], ['i', self.__curent_storage]])
                while self.__xy.isBusy():
                    pass
                #************************************************************************************
                pass
            elif(code[0] == "R"):
                # convert web coordinate to physical coordinate
                x = 10 - int(code[3])
                y = 10 - int(code[1])
                #Remove a Piece from the board in the location of x.y the next three chars in string
                #***********************************************************************************
                #remove_piece_from_gameboard(x,y)
                #************************************************************************************            
                pass
            elif(code == "Skip"):
                #opponent decided not to play their turn
                self.__lcd.lcd_clear()
                self.__lcd.lcd_display_string("Opponent Skipped", 1)
                self.__lcd.lcd_display_string(" their turn", 2)
                pass
            elif(code[0] == "!"):
                #launch end game stage or
                #opponent surrendered 
                return("!")
            elif(code[0] == "B"):
                #last two digits are blacks score
                self.__black_score =  code[-2:]
                logging.info("[main]black score: " + str(self.__black_score))
            elif(code[0] == "W"):
                #last two digits are blacks score
                self.__white_score =  code[-2:]
                logging.info("[main]white score: " + str(self.__white_score))
                if(self.__white_score < self.__black_score):
                    #black won 
                    return "B"
                else:
                    #white won
                    return "W"
            elif(code == "FAIL"):
                return("FAIL")
        return()

    def setup(self, socket_obj, xy_obj, pl_obj, encoder_obj, lcd_obj):
        self.__socket = socket_obj
        self.__xy = xy_obj
        self.__pl = pl_obj
        self.__encoder = encoder_obj
        self.__lcd = lcd_obj
    
    def startGame(self):
        # reset scores
        self.__black_score = 0
        self.__white_score = 0

        # socket init
        self.__socket.connect()
        self.__socket.send_data(bytes(self.__mycolour, "utf-8"))
        data = self.__socket.read_data().decode("utf-8")
        self.__socket.close_socket()
        logging.info("[main]From server: " + data)

        # decode local colour and turn
        for i in range(0, len(data), 4):
            code = data[i:i+4]
            if(code == "0000"):
                # I go first
                self.__turn = 0
            elif(code == "1111"):
                #I go second
                self.__turn = 1
            elif(code == "Blac"):
                self.__mycolour = "Blac"
                self.__curent_storage = 4
                logging.info("[main]I am Black")
                
                self.__lcd.lcd_clear()
                self.__lcd.lcd_display_string("Colour: Black", 1)
                self.__lcd.lcd_display_string("You Go First", 2)
               
            elif(code == "Whit"):
                self.__mycolour = "Whit"
                self.__curent_storage = 1
                logging.info("[main]I am White")
                
                self.__lcd.lcd_clear()
                self.__lcd.lcd_display_string("Colour: White", 1)
                self.__lcd.lcd_display_string("You Go Second", 2)
        
        # this is only needed when going second so that you are listening
        if(self.__turn == 1):
            self.__sendPiece("void")
        
        # let the selector wait at the idle space
        self.__xy.executeCmd(["z0", ['x', 9], ['i', self.__curent_storage]])
        # have to wait until the init finished
        while self.__xy.isBusy():
            pass
        
        while True:
            # play our piece
            # wait for a new piece from local player
            logging.info("[main]waiting for a new piece from local player")
            while not self.__pl.isNewPiece():
                time.sleep(0.5)
                ## need to think about how to integrate the encoder and LCD here
            
            # get the new piece coordinate
            newCoordinate = self.__pl.getNewCoordinate()
            logging.info("[main]new coordinate: " + str(newCoordinate))

            # need to convert to the coordinate format for web interface
            convertedCoordinate = [10-newCoordinate[1], 10-newCoordinate[0]]
            logging.info("[main]converted coordinate: " + str(convertedCoordinate))
            move = str(convertedCoordinate[0]) + "." + str(convertedCoordinate[1])

            #send Piece move
            result = self.__sendPiece(move)
            if result == "!":
                self.__sendPiece("void")
                break
            elif result == "FAIL":
                logging.info("Connection Lost")
                break

            result = self.__sendPiece("void")
            if result == "!":
                break
            elif result == "FAIL":
                logging.info("Connection Lost")
                break
        if result != "FAIL":
            winner = self.__sendPiece("WINR")
            if winner == "B":
                logging.info("Black Won!")
                #*******************************************************
                #LCD_Print("Game Over Black Won")
                #*******************************************************
                self.__lcd.lcd_clear()
                self.__lcd.lcd_display_string("Game Over", 1)
                self.__lcd.lcd_display_string("Black Won", 2)
            elif winner == "W":
                logging.info("White Won!")
                self.__lcd.lcd_clear()
                self.__lcd.lcd_display_string("Game Over", 1)
                self.__lcd.lcd_display_string("White Won", 2)
            else:
                logging.info("error in final score")


        







