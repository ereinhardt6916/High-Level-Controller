import serial

class Piece_locator:

    def __init__(self, port):
        self.port = port
        self.baud_rate = 9600
        self.connection = serial.Serial(self.port, self.baud_rate, timeout=2)
        self.connection.flush()
        self.data_array = []
        for i in range(0, 9):
            new = []
            for j in range(0, 9):
                new.append(1)
            self.data_array.append(new)
    
    def scan_board(self):
        self.connection.write(b"scan\n")
        self.data = self.connection.readline().decode('utf-8').rstrip()

    def print_data(self):
        self.scan_board()
        self.convertToArray()
        print(self.data_array)
    
    def convertToArray(self):
        x = 0
        y = 0

        for bit in self.data:
            if bit == '1':
                self.data_array[x][y] = 1
            else:
                self.data_array[x][y] = 0
            x += 1
            if x > 8:
                x = 0
                y += 1
                if y > 8:
                    break
