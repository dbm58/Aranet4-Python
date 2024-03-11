import argparse

#  device=aranet4:xx:xx:xx:xx
#  device should be an array
#  pass in a dictionary of devices
#  pass in a dictionary of outputs:w

class Parser:

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser("bridge")
        parser.add_argument("devices", nargs="+", action="store")
        parser.add_argument("-o", "--output", nargs="+", action="store")
        args = parser.parse_args()
        return args
