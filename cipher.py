import math


class CodeRing:
    def __init__(self):
        self.encoded = []
        self.password = []
        pass

    def encodeChr(self, character):
        return ord(character)

    def decodeChr(self, integer):
        return chr(integer)

    def encodeLine(self, line):
        encMSG = []
        for index, char in enumerate(line):
            intEncoded = self.encodeChr(char)
            mutator = self.password[index % len(self.password)]
            intEncoded = ((intEncoded * intEncoded) + (mutator * mutator))/89 #89 is prime, makes the number smaller, can mutate some chars due to rounding though. Not an issue in most cases though...
            encMSG.append(intEncoded-97) #removing prime number to lower the integer values below 256
        return encMSG

    def decodeLine(self, tupleEnc):
        buff = []
        if self.password == []:
            return "could not decode wihout password"
        for index, char in enumerate(tupleEnc.split(",")):
            intEncoded = int(char)+97 # adding back
            intEncoded = intEncoded * 89 
            mutator = self.password[index % len(self.password)]
            mutator = mutator * mutator
            intDecoded = intEncoded - mutator
            decoded = math.sqrt(intDecoded)
            buff.append(chr(int(decoded)+1)) #undoing the mutations seems to round everything down. Adding one takes care of that.
        return ''.join(buff)

    def setPass(self, password):
        self.password = [self.encodeChr(x) for x in password]
        pass
