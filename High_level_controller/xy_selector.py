import serial
import threading
import logging
import sys

class XY_selector:

    def __init__(self, port):
        self.__port = port
        self.__baud_rate = 9600
        self.__connection = serial.Serial(self.__port, self.__baud_rate, timeout=20)
        self.__connection.flush()
        self.__cmd_sequence = [] # example: [[x,1], [y,6], [s,2,3],...]
        self.__busy_flag = False
        self.__lock = threading.Lock()

        # init check
        self.__check()
        try:
            self.__listen()
        except Exception as e:
            logging.info("[main]xy selector init error: " + str(e))
            sys.exit("Exit due to error")
    
    def __xMoveTo(self, x_target):
        if x_target > 9:
            x_target = 9
        elif x_target < 1:
            x_target = 1
        self.__connection.write(f"x{x_target}".encode('utf-8'))
    
    def __yMoveTo(self, y_target):
        if y_target > 9:
            y_target = 9
        elif y_target < 1:
            y_target = 1
        self.__connection.write(f"y{y_target}".encode('utf-8'))
    
    def __zUp(self):
        self.__connection.write("z1".encode('utf-8'))

    def __zDown(self):
        self.__connection.write("z0".encode('utf-8'))
    
    def __getPiece(self, storage, rtn_pos):
        if storage > 4:
            storage = 4
        elif storage < 1:
            storage = 1
        
        if rtn_pos > 9:
            rtn_pos = 9
        elif rtn_pos < 1:
            rtn_pos = 1
        self.__connection.write(f"s{storage}.{rtn_pos}".encode('utf-8'))
    
    def __home(self):
        self.__connection.write("home".encode('utf-8'))

    def __fix(self):
        self.__connection.write("fix".encode('utf-8'))

    def __check(self):
        self.__connection.write("check".encode('utf-8'))
    
    def __listen(self):
        return self.__connection.readline().decode('utf-8').rstrip()

    def __executeCmd(self):
        with self.__lock:
            for item in self.__cmd_sequence:
                # send a command to the xy system
                logging.info("[thread]cmd: " + str(item))
                if isinstance(item, str):
                    if item == "home":
                        self.__home()
                    elif item == "fix":
                        self.__fix()
                    elif item == "z1":
                        self.__zUp()
                    elif item == "z0":
                        self.__zDown()
                    else:
                        break
                elif isinstance(item, list): 
                    if item[0] == 'x':
                        self.__xMoveTo(item[1])
                    elif item[0] == 'y':
                        self.__yMoveTo(item[1])
                    elif item[0] == 's':
                        self.__getPiece(item[1], item[2])
                    else:
                        break
                else:
                    break
                
                # wait for feedback
                try:
                    feedback = self.__listen()
                    logging.info("[thread]feedback: " + feedback)
                except Exception as e:
                    logging.info("[thread]XY system error" + str(e))
                    break
            else:
                logging.info("[thread]All cmds are sent")
            
            self.__busy_flag = False


    def executeCmd(self, cmds):
        # example: [[x,1], [y,6], [s,2,3], "home"...]
        with self.__lock:
            self.__cmd_sequence = cmds
            self.__busy_flag = True
        execThrd = threading.Thread(target=self.__executeCmd, daemon=True)
        execThrd.start()
        logging.info("[main]xy exec thread started")


                
