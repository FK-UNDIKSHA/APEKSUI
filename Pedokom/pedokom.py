# Importing Libraries
import serial
import time

class PedoKom:
    def __init__(self, ports, bauds, timeouts):
        self.port       = ports             #'/dev/ttyUSB0'
        self.baud       = bauds
        self.timeout    = timeouts
        self.arduino    = serial.Serial(port=self.port, baudrate=self.baud, timeout=self.timeout)
        time.sleep(1)

    def write_read(self, x, s=5):
        """
        Handle Serial Communication Between Arduino and Python
        """
        self.arduino.write(bytes(x, 'utf-8'))
        if s > 0:
            time.sleep(s) #set to 2 second to avoid latency problem?, simply to wait from arduino response
            data = self.arduino.readline()
            return data
        else:
            return 1

    def SendCommand(self, cmd: str, s:float=5) -> dict:
        """
        Send Command To Arduino Mega Through Serial Communication
        If You Want To Add More Command , Please Refer to the .ino document

        This is only command sender and receiver,
        The rest will handled by the arduino
        """
        value = self.write_read(cmd).decode('utf-8')
        return {"Command": cmd, "Response": value}

if __name__ == "__main__":
    #DEBUG PURPOSE
    #print(SendCommand("pesan;yuhuu saya ada disini bro"))
    coms = PedoKom('/dev/ttyUSB0', 9600, .1)
    while True:
        #Making General Command
        num = input("Arduino Command: ") # Taking input from user
        print("Waiting...")
        value = coms.write_read(num)
        print(value.decode()) # printing the value
