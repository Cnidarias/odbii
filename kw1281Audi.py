import os
import serial
import time
import struct
import sys
import threading


class kw1281(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.ser = None
        self.state = 0
        self.ecuOpen = -1
        address = ("localhost", 6000)
        self.data = data

    def run(self):
        try:
            self.ser = serial.Serial(
                "/dev/ttyUSB0", 9600, timeout=1, rtscts=1, dsrdtr=1
            )
            self.packetCounter = 0

            self.state = 1
            self.mainRunner()
        except:
            if self.ser is not None:
                self.ser.close()
            # raise
            return

    def bitFlip(self, n):
        return chr(0xFF ^ n)

    def sendBit(self, bit):
        if bit == 1:
            self.ser.setRTS(True)
            self.ser.setBreak(False)
            self.ser.setRTS(False)

        if bit == 0:
            self.ser.setRTS(True)
            self.ser.setBreak(True)

    def sendACKBlock(self):
        if self.packetCounter == 0xFF:
            self.packetCounter = 0
        else:
            self.packetCounter += 1

        self.ser.write("\x03")
        packet = self.ser.read(1)

        packet = self.ser.read(1)  # should be 0x03 kompliment

        self.ser.write(chr(self.packetCounter))
        packet = self.ser.read(1)

        packet = self.ser.read(1)  # should be self.packetCounter kompliment

        self.ser.write("\x09")  # this is the block command
        packet = self.ser.read(1)
        packet = self.ser.read(1)  # should be the 0x09 kompliment

        self.ser.write("\x03")
        packet = self.ser.read(1)

    def sendQuitBlock(self):
        if self.packetCounter == 0xFF:
            self.packetCounter = 0
        else:
            self.packetCounter += 1

        self.ser.write("\x03")
        self.ser.read(1)

        packet = self.ser.read(1)  # should be 0x03 compliment

        self.ser.write(chr(self.packetCounter))
        packet = self.ser.read(1)  # should be self.packetCounter kompliment

        self.ser.write("\x06")
        self.ser.read(1)

        packet = self.ser.read(1)  # should be 0x06 compliment

        self.ser.write("\x03")
        packet = self.ser.read(1)

    def requestDataBlock(self, block):
        if self.packetCounter == 0xFF:
            self.packetCounter = 0
        else:
            self.packetCounter += 1

        self.ser.write("\x04")
        packet = self.ser.read(1)

        packet = self.ser.read(1)  # this is the 0x04 kompliment

        self.ser.write(chr(self.packetCounter))
        packet = self.ser.read(1)

        packet = self.ser.read(1)  # this is the kompliment of the self.packetCounter

        self.ser.write("\x29")  # this is the command for a grp reading
        packet = self.ser.read(1)

        packet = self.ser.read(1)  # this is the compliment of 0x29

        # now send the grp ID number --
        self.ser.write(chr(block))
        packet = self.ser.read(1)

        packet = self.ser.read(1)  # should be compliment - yet again

        self.ser.write("\x03")
        packet = self.ser.read(1)

    def readBlock(self):
        #################################################
        packet = self.ser.read(1)
        messageLen = ord(packet)
        self.ser.write(self.bitFlip(messageLen))
        packet = self.ser.read(1)

        packet = self.ser.read(1)
        self.packetCounter = ord(packet)
        self.ser.write(self.bitFlip(self.packetCounter))
        packet = self.ser.read(1)

        packet = self.ser.read(1)
        blockTitle = ord(packet)
        self.ser.write(self.bitFlip(blockTitle))
        packet = self.ser.read(1)

        if blockTitle == 0xF6:
            i = 3
            message = ""

            while i < messageLen:
                packet = self.ser.read(1)
                message += packet

                self.ser.write(self.bitFlip(ord(packet)))
                packet = self.ser.read(1)
                i += 1

            packet = self.ser.read(1)  # read 0x03 end block
            return message

        elif blockTitle == 0x09:
            packet = self.ser.read(1)  # read 0x03 end block
            return "ACK"

        elif blockTitle == 0xE7:
            i = 3
            result = []
            while i < messageLen:
                packet = self.ser.read(1)
                result.append(ord(packet))
                self.ser.write(self.bitFlip(ord(packet)))
                packet = self.ser.read(1)
                i += 1

            packet = self.ser.read(1)  # read 0x03 end block
            return self.humanReadableVals(result)

    ####################################################

    def humanReadableVals(self, array):
        message = "READABLE CAR RET: "
        i = 0
        while i < len(array) / 3:
            index = i * 3
            a = array[index + 1]
            b = array[index + 2]
            value = 0

            if array[index] == 1:
                value = 0.2 * a * b
                message += "Motordrehzahl [rpm] " + str(value) + "\n"
                self.data["rpm"] = value

            elif array[index] == 2 and self.ecuOpen == 0x01:
                value = a * 0.002 * b
                message += "Abs Drosselklast. [%] " + str(value) + "\n"

            elif array[index] == 5:
                value = a * (b - 100) * 0.1
                if self.ecuOpen == 0x01:
                    message += "Oel Temperatur [deg] " + str(value) + "\n"
                elif self.ecuOpen == 0x17:
                    message += "Ausen Temperatur [deg] " + str(value) + "\n"

            elif array[index] == 6:
                value = 0.001 * a * b
                message += "Spannung ECU [V] " + str(value) + "\n"

            elif array[index] == 7:
                value = 0.01 * a * b
                message += "Geschwindigkeit [km/h] " + str(value) + "\n"
                self.data["speed"] = value

            elif array[index] == 8 and self.ecuOpen == 0x01:
                value = 0.1 * a * b
                message += "Cruse control [bool] " + str(value) + "\n"

            elif array[index] == 15 and self.ecuOpen == 0x01:
                value = 0.01 * a * b
                message += "CAN Bus Status [ms] " + str(value) + "\n"

            elif array[index] == 18 and self.ecuOpen == 0x01:
                value = 0.04 * a * b
                message += "Pressure [mbar] " + str(value) + "\n"

            elif array[index] == 19 and self.ecuOpen == 0x17:
                value = a * b * 0.01
                message += "Tank inhalt [L] " + str(value) + "\n"

            elif array[index] == 21 and self.ecuOpen == 0x01:
                value = 0.001 * a * b
                message += "Modul Piston [V] " + str(value) + "\n"

            elif array[index] == 23 and self.ecuOpen == 0x01:
                value = b / 256 * a
                message += "EGR Valve [%] " + str(value) + "\n"

            elif array[index] == 27 and self.ecuOpen == 0x01:
                value = abs(b - 128) * 0.01 * a
                message += "Ign Timing [deg] " + str(value) + "\n"

            elif array[index] == 31 and self.ecuOpen == 0x01:
                value = b / 2560 * a
                message += "Preheating Time [deg] " + str(value) + "\n"

            elif array[index] == 33 and self.ecuOpen == 0x01:
                if a == 0:
                    value = 100 * b
                else:
                    value = 100 * b / a
                message += "Stellung GasPedal [%] " + str(value) + "\n"

            elif array[index] == 35 and self.ecuOpen == 0x01:
                value = 0.01 * a * b
                message += "Verbrauch [l/h] " + str(value) + "\n"
                self.data["usage"] = value

            elif array[index] == 36 and self.ecuOpen == 0x17:
                value = a * 2560 + b * 10
                message += "Ges. Laufleistung [km] " + str(value) + "\n"

            elif array[index] == 39 and self.ecuOpen == 0x01:
                value = b / 256 * a
                message = "Inj Quantitity Driver Req [mg/h] " + str(value) + "\n"

            elif array[index] == 44 and self.ecuOpen == 0x17:
                message += "Uhrzeit " + str(a) + ":" + str(b) + "\n"

            elif array[index] == 49:
                value = (b / 4) * a * 0.1
                message += "Mass Air/Rev [mg/h]" + str(value) + "\n"

            elif array[index] == 53 and self.ecuOpen == 0x01:
                value = (b - 128) * 1.4222 + 0.006 * a
                message += "Luftdurchfluss [g/s] " + str(value) + "\n"

            elif array[index] == 63 and self.ecuOpen == 0x01:
                message = "Text " + str(a) + str(b) + "?" + "\n"

            elif array[index] == 64 and self.ecuOpen == 0x17:
                value = a + b
                message += "Widerstand [ohm] " + str(value) + "\n"

            else:
                message += (
                    "Unknown "
                    + str(array[index])
                    + "a: "
                    + str(a)
                    + "b: "
                    + str(b)
                    + "\n"
                )

            i += 1

        return message

    def mainRunner(self):
        while True:
            # this needs to be revamped
            if self.state == 1:
                if self.ecuOpen != 0x01:
                    self.openECU(0x01)
                    self.ecuOpen = 0x01
                self.sendACKBlock()
                print(self.readBlock())
                self.requestDataBlock(0x03)
                print(self.readBlock())
                self.requestDataBlock(0x0B)
                print(self.readBlock())

                # self.sendQuitBlock()
                # self.state = 2

            if self.state == 2:
                if self.ecuOpen != 0x17:
                    self.openECU(0x17)
                    self.ecuOpen = 0x17
                self.sendACKBlock()
                print(self.readBlock())
                self.requestDataBlock(0x01)
                print(self.readBlock())

                # self.sendQuitBlock()
                # self.state = 1

    def openECU(self, address=0x01):
        delay = 0.2

        # For ECU Address 0x01:
        # need to send 0 1000 000 0 1

        self.sendBit(0)
        time.sleep(delay)

        p = 1
        for i in xrange(0, 7):
            bit = (address >> i) & 0x01
            self.sendBit(bit)

            p ^= bit

            time.sleep(delay)

        self.sendBit(p)
        time.sleep(delay)

        self.sendBit(1)
        time.sleep(delay)

        self.ser.setRTS(False)
        self.ser.setDTR(True)

        time.sleep(0.5)

        self.ser.setRTS(True)
        self.ser.setDTR(True)
        self.ser.setBreak(False)

        # read the bits you sent to "clear" buffer

        # Read stuff that we do not /really/ care about

        # Kennungs ID

        print(address)

        if address == 0x01:
            packet = self.ser.read(1)
            while ord(packet) != 0x8A:
                packet = self.ser.read(1)
                print(str(address) + "\t" + str(ord(packet)))
        else:
            packet = self.ser.read(1)
            while ord(packet) != 0x8A:
                packet = self.ser.read(1)
                print(str(address) + "\t" + str(ord(packet)))
            packet = self.ser.read(1)
            while ord(packet) != 0x8A:
                packet = self.ser.read(1)
                print(str(address) + "\t" + str(ord(packet)))
        self.ser.write(self.bitFlip(ord(packet)))
        packet = self.ser.read(1)  # always throws same packet back at us

        message = self.readBlock()

        # Keep on reading String messages that the ECU sends us, until
        # it is finally done telling us who it is
        # then simply send another ACK block and start reading data - easy
        while message is not "ACK":
            print("This is a message")
            print(message)
            self.sendACKBlock()  # self.send ack block confimration
            message = self.readBlock()

        self.sendACKBlock()
        print(self.readBlock())

        # NOW we have handeled basic communication -
        # We now self.send ACK commands back and forth - forever

        # test all avaibale packets we could self.read
        # tester = 1
        # while tester <= 255:
        #  try:
        #    print tester, self.readBlock()
        #    self.sendACKBlock()
        #    print self.readBlock()
        #    requestDataBlock(tester)
        #    tester += 1
        #  except:
        #    break


#############################################################################
def main():
    data = {
        "speed": 200,
        "rpm": 2000,
        "fuel": 10,
        "mileage": 10,
        "time": "12:12",
        "usage": 3.5,
    }
    task = kw1281(data)
    task.start()


if __name__ == "__main__":
    main()
