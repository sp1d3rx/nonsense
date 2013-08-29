import math

class CodeRing:
    def __init__(self):
        self.encoded = []
        self.password = []
        pass
    def encodeChr(self,character):
        return ord(character)
    def decodeChr(self,integer):
        return chr(integer)
    def encodeLine(self,line):
        encMSG = []
        for index, char in enumerate(line):
            b = ord(char)
            c = self.password[index%len(self.password)]
            b = ((b * b) + (c * c))/89
            encMSG.append(b-97)
        return encMSG
    def decodeLine(self,tupleEnc):
        buff = []
        if self.password == []:
            return "could not decode wihout password"
        for index, char in enumerate(tupleEnc.split(",")):
            d = int(char)+97
            d = d * 89
            c = self.password[index%len(self.password)]
            c = c * c
            a = d - c
            decoded = math.sqrt(a)
            buff.append(chr(int(decoded)+1))
        return ''.join(buff)

    def setKey(self,keycode):
        self.key = keycode
        self.key = self.key * 97
    def setPass(self,password):
        self.password = [self.encodeChr(x) for x in password]
        pass
