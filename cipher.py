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
            intEncoded = (
                (intEncoded * intEncoded) + (mutator * mutator)
            ) / 89  # 89 is prime, makes the number smaller, can mutate some chars due to rounding though. Not an issue in most cases though...
            encMSG.append(
                intEncoded - 97
            )  # removing prime number to lower the integer values below 256
        return [int(math.floor(flt)) for flt in encMSG]

    def decodeLine(self, tupleEnc):
        if type(tupleEnc) == list:
            print("found list type")
            tupleEnc = ",".join(str(x) for x in tupleEnc)
        buff = []
        if self.password == []:
            return "could not decode wihout password"
        for index, char in enumerate(tupleEnc.split(",")):
            intEncoded = int(char) + 97  # adding back
            intEncoded = intEncoded * 89
            mutator = self.password[index % len(self.password)]
            mutator = mutator * mutator
            intDecoded = intEncoded - mutator
            decoded = math.sqrt(intDecoded)
            buff.append(
                chr(int(decoded) + 1)
            )  # undoing the mutations seems to round everything down. Adding one takes care of that.
        return "".join(buff)

    def setPass(self, password):
        self.password = [self.encodeChr(x) for x in password]
        pass


if __name__ == "__main__":
    cr = CodeRing()
    cr.setPass("HWre0IXm0Ju ln6vial4!ik4xpqKdV7tOOd.ymXw7BcohwxWFXABogT,c8loMbPfWAs")
    enctuple = cr.encodeLine("Alice, walk to the store and get me some milk, cheese, and anchovies.")
    decstring = cr.decodeLine(enctuple)
    print(enctuple)
    print(decstring)
