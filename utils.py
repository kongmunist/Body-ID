import serial
import sys
import threading
import binascii
import hashlib as hl
from stringVersion import condense, findSmallest

# Taken from my friend Sam, god bless his soul
# fast serial readline from https://github.com/pyserial/pyserial/issues/216#issuecomment-369414522
class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i + 1]
                self.buf[0:] = data[i + 1:]
                return r
            else:
                self.buf.extend(data)

class IdManager():
    def __init__(self):
        self.people = ["andy", "tom", "david", "vignesh"]
        # self.peoplehash = {x:str(abs(hash(x))).ljust(20, "0") for x in self.people}
        self.peoplehash = {x:'1'+ hl.md5(x.encode('utf-8')).hexdigest() for x in self.people}
        print("Known people hashes:")
        for name in self.people:
            print("{} -> {}".format(name, self.getIDBinaryFromName(name)))
        print("")
        # peopleAscii = []

    def getID(self, str):
        return self.peoplehash[str]
        # 3455203352929927801000000

    def getIDBinaryFromName(self, str):
        return self.getIDBinaryFromHash(self.peoplehash[str])

    def getIDBinaryFromHash(self, str):
        return ''.join(format(ord(i), 'b') for i in str)


    def findClosestMatch(self, str):
        str = str.ljust(33, "0")
        read_b = self.getIDBinaryFromHash(str)

        closest = None
        minDist = 10000000000000
        for name in self.peoplehash.keys():
            candidate_b = self.getIDBinaryFromName(name)
            dist = 0
            for i in range(len(read_b)):
                if read_b[i] != candidate_b[i]:
                    dist+=1
            if dist < minDist:
                minDist = dist
                closest = name
        return closest


            # dist = bitcount(val ^ str)











# stoppable thread for serial tx/rx
class SerialThread(threading.Thread):
    def __init__(self, port, dataHolder):
        super(SerialThread, self).__init__()
        self._stop = threading.Event()
        self.port = port
        self.serialData = ""
        self.FESData = None
        self.dataHolder = dataHolder
        self.data = []


        self.peopleFinder = IdManager()

        self.i = 0

        self.recording = False

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.RTS = False
        msg = []

        try:
            # self.com = serial.Serial(self.port, 115200)
            self.com = serial.Serial(self.port, 115200)
            self.rl = ReadLine(self.com)
        except:
            print("\nSERIAL PORT ERROR")
            sys.exit()
        while True:
            if self.stopped():
                return

            # readline, parse csv. Can read different format if preferable
            self.serialData = self.rl.readline().decode("utf-8")  # .strip()#.split(",")
            if self.recording:
                self.data.append(int(self.serialData.strip()))
            try:
                if self.serialData != "":
                    self.dataHolder.append(int(self.serialData.strip()))
                    self.i += 1
                    if self.i % 20 == 0:
                        tmp = "".join([str(x) for x in list(self.dataHolder)][:500])
                        # tmp = "".join([str(x) for x in list(self.dataHolder)])
                        n = condense(tmp, findSmallest(tmp))
                        n = int(n,2)

                        hex = binascii.unhexlify('%x' % n)
                        tmpstring = "".join([chr(x) for x in hex if x >64 and x < 123])
                        if len(tmpstring) > 2:
                            print(tmpstring)
                            print()

            except Exception as e:
                pass

            empty = True
            if len(self.serialData) > 2: # remove this condition later
                empty = False