import sys


class BufferedPrinter:
    def __init__(self):
        self.buff = []

    def start(self):
        self.oldstdout = sys.stdout
        sys.stdout = self

    def end(self):
        sys.stdout = self.oldstdout
        print("".join(self.buff), end="")
        self.buff.clear()

    def write(self, s):
        self.buff.append(s)

    def flush(self):
        pass
