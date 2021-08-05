import socket
import logging
from threading import Thread, Lock
import time
import os

class Watchdog_client:

    def __init__(self):
        self.__port = 10237
        self.__host = "127.0.0.1"
        self.Smutex = Lock()
        self.Vmutex = Lock()
        self.Sfail_flag = False
        self.Vfail_flag = False
        self.stop_flag = False

    def start(self, lcd):
        self.W_thread = Thread(target=self.__watchdog_start, daemon=True)
        self.W_thread.start()
        self.__lcd = lcd

    def stop(self):
        self.stop_flag = True
        self.W_thread.join()
    
    # periodically send 0 to server
    # expect to receive 0 -- normal
    #                   1 -- virtual side disconnected

    def __watchdog_start(self):
        self.socket = self.Shelper(self.__host, self.__port)
        logging.info("[W]Watchdog started")

        while True:
            try:
                self.socket.connect()
                break
            except:
                pass
        
        logging.info("[W]Watchdog server connected")
        failure_counter = 0

        while not self.stop_flag:
            try:
                self.socket.send_data(0)
                result = self.socket.read_data()
                if result == 1:
                    # virtual side disconnected
                    failure_counter += 1
                    if failure_counter >= 3:
                        self.Vmutex.acquire()
                        self.Vfail_flag = True
                        self.Vmutex.release()
                        logging.info("[W]Virtual board connection lost")
                        self.__lcd.lcd_clear()
                        self.__lcd.lcd_display_string("Virtual Board", 1)
                        self.__lcd.lcd_display_string("Connection Lost", 2)
                        break
                elif result == 2:
                    # server connection lost
                    self.Smutex.acquire()
                    self.Sfail_flag = True
                    self.Smutex.release()
                    logging.info("[W]Server connection lost")
                    self.__lcd.lcd_clear()
                    self.__lcd.lcd_display_string("Control Server", 1)
                    self.__lcd.lcd_display_string("Connection Lost", 2)
                    break
                else:
                    # everything is normal
                    failure_counter = 0
                
                self.Vmutex.acquire()
                self.Smutex.acquire()
                logging.info(f"[W]Received: {result} failure_counter: {failure_counter} Sflag: {self.Sfail_flag} Vflag: {self.Vfail_flag}")
                self.Smutex.release()
                self.Vmutex.release()

                # ping about every 2 seconds
                time.sleep(2)

            except Exception as e:
                logging.info("[W]"+str(e))
                 # server connection lost
                self.Smutex.acquire()
                self.Sfail_flag = True
                self.Smutex.release()
                break
        
        logging.info("[W]Socket closed")
        self.socket.close_socket()
        os.system("pkill python")

    class Shelper:
        def __init__(self, host, port):
            self.__host = host
            self.__port = port

        def connect(self):
            self.__sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sckt.settimeout(30)
            self.__sckt.connect((self.__host, self.__port))

        def send_data(self, content):
            self.__sckt.send(bytes(str(content), "utf-8"))

        def read_data(self):
            try:
                buf = self.__sckt.recv(1024)
                return int(buf.decode("utf-8"))
            except:
                # other connection issues
                return 2

        def close_socket(self):
            self.__sckt.close()
            logging.info("[main]socket closed")