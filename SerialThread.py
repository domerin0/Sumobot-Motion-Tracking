import threading
import serial

class SerialThread(threading.Thread):
    def __init__(self):
        super(SerialThread, self).__init__()
        self.value = 0
        self.daemon = True
        self.ser = serial.Serial('/dev/ttyACM0', 9600)

    def run(self):
        try:
            self.ser.write(str(self.value))
        except Exception as e:
            print str(e)
   
    def addValue(self, value):
        self.value = value
        self.start()
