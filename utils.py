import serial
import sys
import threading
import binascii
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
                        tmp = "".join([str(x) for x in list(self.dataHolder)][:300])
                        n = int(tmp,2)

                        # print(binascii.unhexlify('%x' % n))
                        print(condense(tmp, findSmallest(tmp)))
                        print("tmp", tmp)

                        # print("".join([str(x) for x in list(self.dataHolder)][:200]))
            except Exception as e:
                pass

            empty = True
            if len(self.serialData) > 2: # remove this condition later
                empty = False