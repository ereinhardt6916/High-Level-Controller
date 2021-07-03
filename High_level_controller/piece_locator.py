import serial
import logging

class Piece_locator:

    def __init__(self, port):
        self.__port = port
        self.__baud_rate = 9600
        self.__connection = serial.Serial(self.__port, self.__baud_rate, timeout=2)
        self.__connection.flush()
        self.__newPieceCoordinate = [0, 0]
        self.__piece_flag = False
        self.__data_array = []        #for raw data
        self.__piece_array = []       #for processed data
        logging.info("[main]piece_locator initialized.")
        
        # init the two arrays
        for i in range(0, 9):
            new = []
            new2 = []
            for j in range(0, 9):
                new.append(1)
                new2.append(1)
            self.__data_array.append(new)
            self.__piece_array.append(new2)
    
    def __scan_board(self):
        self.__connection.write(b"scan\n")
        self.data = self.__connection.readline().decode('utf-8').rstrip()
        self.__convertToArray()
        self.__processData()
    
    def __convertToArray(self):
        x = 0
        y = 0

        for bit in self.data:
            if bit == '1':
                self.__data_array[x][y] = 1
            else:
                self.__data_array[x][y] = 0
            x += 1
            if x > 8:
                x = 0
                y += 1
                if y > 8:
                    break
    
    def __processData(self):
        for y in range(len(self.__data_array)):
            for x in range(len(self.__data_array[y])):
                ## can only change to zero, not vice versa
                if (self.__data_array[x][y] == 0) and (self.__piece_array[x][y] != 0):
                    self.__piece_array[x][y] = 0
                    self.__newPieceCoordinate[0] = x
                    self.__newPieceCoordinate[1] = y
                    self.__piece_flag = True

    def resetCoordinate(self, x, y):
        self.__piece_array[x-1][y-1] = 1

    def setCoordinate(self, x, y):
        self.__piece_array[x-1][y-1] = 0

    def getNewCoordinate(self):
        # self.__scan_board()
        self.__piece_flag = False
        return [self.__newPieceCoordinate[0]+1, self.__newPieceCoordinate[1]+1]
    
    def getPieceLayout(self):
        self.__scan_board()
        return self.__piece_array
    
    def print_data(self):
        self.__scan_board()
        print(self.__piece_array)
    
    def isNewPiece(self):
        self.__scan_board()
        return self.__piece_flag

    