import logging
import time
from addPiece import add_piece_moves_wrapper, remove_piece_moves_wrapper, add_piece_to_array
from datetime import datetime

class GameManager:
    def __init__(self):
        self.__mycolour = "Blac"
        self.__myColourCode = 1
        self.__turn = 1
        self.__white_score = 0
        self.__black_score = 0
        self.__curent_storage = 1
        self.__pieceColourPosition = 1
        self.__lcdScenario = 1
        self.__buttonPushedFlag = False
        self.__colourSelectTime = 30
        self.__turnTime = 120
        self.__restartTime = 10
        self.__surrenderOptPosition = 1
        self.__lastPushTime = datetime.now()
    
    def __sendPiece(self, pieceAdded):
        self.__socket.connect()
        self.__socket.send_data(bytes(pieceAdded, "utf-8"))
        logging.info("[main]To server: " + str(pieceAdded))

        logging.info("[main]waiting for server response")
        return self.__receMesg()
    
    def __cmdConversion(self, listOfCmds):
        for cmd in listOfCmds:
            if isinstance(cmd, list):
                if cmd[0] == 'x':
                    cmd[0] = 'y'
                    cmd[1] = 10 - cmd[1]
                elif cmd[0] == 'y':
                    cmd[0] = 'x'
                    cmd[1] = 10 - cmd[1]
        
        return listOfCmds

    def __receMesg(self):
        data = self.__socket.read_data()
        mesg = data.decode("utf-8")
        logging.info("[main]From server: " + mesg)
        self.__socket.close_socket()

        for i in range(0, len(mesg), 4):
            code = mesg[i:i+4]
            if(code[0] == "A"):
                x_web = int(code[1])
                y_web = int(code[3])
                x_phys = 10 - y_web
                y_phys = 10 - x_web
                #add a Piece to the board in the location of x.y the next three chars in string
                #***********************************************************************************
                # set the piece coordinate in the piece locator, otherwise it considers it is a new piece from the local player
                self.__pl.setCoordinate(x_phys, y_phys)

                ## get list of commands from path algorithm
                listOfCmds = add_piece_moves_wrapper(x_web, y_web, (3-self.__myColourCode))

                ## convert list of command for physical board
                listOfCmds = self.__cmdConversion(listOfCmds)

                ## append the final actions
                listOfCmds += ['i' + str(self.__curent_storage)]
                logging.info(listOfCmds)
                
                ## send out to execute
                # wait until the xy system not busy
                while self.__xy.isBusy():
                    pass
                self.__xy.executeCmd(listOfCmds)
                while self.__xy.isBusy():
                    pass
                #************************************************************************************
                
            elif(code[0] == "R"):
                x_web = int(code[1])
                y_web = int(code[3])
                x_phys = 10 - y_web
                y_phys = 10 - x_web
                #Remove a Piece from the board in the location of x.y the next three chars in string
                self.__pl.resetCoordinate(x_phys, y_phys)
                
                ## get list of commands from path algorithm
                listOfCmds = remove_piece_moves_wrapper(x_web, y_web)

                ## convert list of command for physical board
                listOfCmds = self.__cmdConversion(listOfCmds)

                ## append the final actions
                listOfCmds += ['i' + str(self.__curent_storage)]
                logging.info(listOfCmds)

                ## send out to execute
                # wait until the xy system not busy
                while self.__xy.isBusy():
                    pass
                self.__xy.executeCmd(listOfCmds)
                while self.__xy.isBusy():
                    pass

                
            elif(code == "Skip"):
                #opponent decided not to play their turn
                # self.__lcd.lcd_clear()
                # self.__lcd.lcd_display_string("Opponent Skipped", 1)
                # self.__lcd.lcd_display_string(" their turn", 2)
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
        
        # wait a button push to start a new game
        self.__buttonPushedFlag = False
        self.__lcdScenario = 1
        self.__lcd.lcd_display_string("Push to start a ", 1)
        self.__lcd.lcd_display_string("new game.       ", 2)
        while not self.__buttonPushedFlag:
            pass
        self.__buttonPushedFlag = False

        # reset scores
        self.__black_score = 0
        self.__white_score = 0

        # socket init
        self.__lcd.lcd_clear()
        self.__lcd.lcd_display_string("Connecting", 1)
        try:
            self.__socket.connect()
        except:
            logging.info("server not available")
            countdown = 5
            while countdown > 0:
                logging.info(f"Retry after {countdown} seconds")
                countdown -= 1
                time.sleep(1)
            return
        self.__lcd.lcd_clear()
        self.__lcd.lcd_display_string("Server Connected", 1)
        time.sleep(2)

        # choose physical board piece colour
        countdown = self.__colourSelectTime
        self.__lcdScenario = 2
        logging.info("[main]Choosing colour from LCD")
        while countdown > 0:
            # self.__lcd.lcd_clear_line(1)
            self.__lcd.lcd_display_string("Yr Colour({0}):   ".format(int(countdown)), 1)
            # self.__lcd.lcd_clear_line(2)
            if self.__pieceColourPosition == 1:
                self.__lcd.lcd_display_string(" >Black  White", 2)
            elif self.__pieceColourPosition == 2:
                self.__lcd.lcd_display_string("  Black >White", 2)

            if self.__buttonPushedFlag:
                self.__buttonPushedFlag = False
                break
            time.sleep(0.2)
            countdown -= 0.2
        
        self.__lcd.lcd_clear()
        self.__lcd.lcd_display_string("Waiting for the", 1)
        self.__lcd.lcd_display_string("other player", 2)

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
                self.__myColourCode = 1
                self.__curent_storage = 2
                logging.info("[main]I am Black")
                
                self.__lcd.lcd_clear()
                self.__lcd.lcd_display_string("Colour: Black", 1)
                self.__lcd.lcd_display_string("You Go First", 2)
               
            elif(code == "Whit"):
                self.__mycolour = "Whit"
                self.__myColourCode = 2
                self.__curent_storage = 1
                logging.info("[main]I am White")
                
                self.__lcd.lcd_clear()
                self.__lcd.lcd_display_string("Colour: White", 1)
                self.__lcd.lcd_display_string("You Go Second", 2)

                time.sleep(2)
                # display wait for opponent's move message
                self.__lcd.lcd_display_string("Wait for your   ", 1)
                self.__lcd.lcd_display_string("opponent's move ", 2)
        
        # this is only needed when going second so that you are listening
        if(self.__turn == 1):
            self.__sendPiece("void")
        
        # let the selector wait at the idle space
        self.__xy.executeCmd(["z0", ['x', 9], 'i'+ str(self.__curent_storage)])
        # have to wait until the init finished
        while self.__xy.isBusy():
            pass
        
        while True:
            surrenderFlag = False

            # play our piece
            # wait for a new piece from local player
            logging.info("[main]waiting for a new piece from local player")
            self.__lcdScenario = 3
            countdown = self.__turnTime
            self.__lcd.lcd_clear()
            startTime = datetime.now()
            timeDiff = 0
            while countdown > timeDiff:
                if self.__lcdScenario == 3: 
                    self.__lcd.lcd_display_string("Your turn!      ", 1)
                    self.__lcd.lcd_display_string("Time: " + str(countdown-int(timeDiff))+"     ", 2)
                else:
                    # enter scenario 4, confirm surrender
                    self.__lcd.lcd_display_string("Surrender?("+str(countdown-int(timeDiff))+")  ", 1)
                    if self.__surrenderOptPosition == 1:
                        self.__lcd.lcd_display_string(">No  Yes      ", 2)
                        if self.__buttonPushedFlag:
                            # go back to scenario 3
                            self.__lcdScenario = 3
                            self.__buttonPushedFlag = False
                            time.sleep(0.2)
                    elif self.__surrenderOptPosition == 2:
                        self.__lcd.lcd_display_string(" No >Yes      ", 2)
                        if self.__buttonPushedFlag:
                            surrenderFlag = True
                            self.__buttonPushedFlag = False
                            self.__surrenderOptPosition = 1
                            break

                if self.__pl.isNewPiece():
                    break
                timeDiff = datetime.now() - startTime
                timeDiff = timeDiff.seconds + timeDiff.microseconds/1000000
            else:
                surrenderFlag = True

            if not surrenderFlag:
                # get the new piece coordinate
                newCoordinate = self.__pl.getNewCoordinate()
                logging.info("[main]new coordinate: " + str(newCoordinate))

                # update the addPiece algorithm
                add_piece_to_array(10-newCoordinate[1], 10-newCoordinate[0], self.__myColourCode)

                # need to convert to the coordinate format for web interface
                convertedCoordinate = [10-newCoordinate[1], 10-newCoordinate[0]]
                logging.info("[main]converted coordinate: " + str(convertedCoordinate))
                move = str(convertedCoordinate[0]) + "." + str(convertedCoordinate[1])
                
                # display wait for opponent's move message
                self.__lcd.lcd_display_string("Wait for your   ", 1)
                self.__lcd.lcd_display_string("opponent's move ", 2)
            else:
                move = "!sur"

            #send Piece move
            result = self.__sendPiece(move)
            if result == "FAIL":
                logging.info("Connection Lost")
                break
            elif result != "!" and result != "B" and result != "W":

                result = self.__sendPiece("void")
                if result == "FAIL":
                    logging.info("Connection Lost")
                    break

            if result == "!" or result == "B" or result == "W":
                if result == "!":
                    winner = self.__sendPiece("void")
                    winner = self.__sendPiece("WINR")
                else:
                    winner = result
                self.__lcd.lcd_clear()
                if winner == "B":
                    logging.info("Black Won!")
                    #*******************************************************
                    #LCD_Print("Game Over Black Won")
                    #*******************************************************   
                    self.__lcd.lcd_display_string("Black Won", 1)
                elif winner == "W":
                    logging.info("White Won!")
                    self.__lcd.lcd_display_string("White Won", 1)
                else:
                    logging.info("error in final score")
                countdown = self.__restartTime
                while countdown > 0:
                    if countdown > 0.7*self.__restartTime:
                        self.__lcd.lcd_display_string(f"Game Over({countdown})  ", 2)
                    else:
                        self.__lcd.lcd_display_string(f"B:{self.__black_score} W:{self.__white_score}({countdown})  ", 2)
                    time.sleep(1)
                    countdown -= 1
                break

    def encoderTriggered(self, value):
        if self.__lcdScenario == 2:
            if self.__pieceColourPosition == 1:
                self.__pieceColourPosition = 2
                # logging.info("position 2")
            else:
                self.__pieceColourPosition = 1
                # logging.info("position 1")
        elif self.__lcdScenario == 4:
            if self.__surrenderOptPosition == 1:
                self.__surrenderOptPosition = 2
            else:
                self.__surrenderOptPosition = 1

    def buttonPushed(self):
        now = datetime.now()
        timeDiff = now - self.__lastPushTime
        self.__lastPushTime = now
        timeDiff = timeDiff.seconds + timeDiff.microseconds/1000000
        logging.info("Button Pushed" + str(timeDiff))
        if timeDiff > 0.5:
            if self.__lcdScenario == 1:
                self.__buttonPushedFlag = True
            elif self.__lcdScenario == 2:
                if self.__pieceColourPosition == 1:
                    self.__mycolour = "Blac"
                    self.__myColourCode = 1
                else:
                    self.__mycolour = "Whit"
                    self.__myColourCode = 2
                self.__buttonPushedFlag = True
            elif self.__lcdScenario == 3:
                self.__lcdScenario = 4
            elif self.__lcdScenario == 4:
                self.__buttonPushedFlag = True



        







