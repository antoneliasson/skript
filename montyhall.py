#!/usr/bin/env python
#
# Beräknar sannolikheten för Monty Hall-problemet för ett givet antal dörrar.
#
# Skrivet den 5 december 2012.
# (c) Anton Eliasson
from fractions import Fraction
import sys

class MontyHall:
    def __init__(self, prize, selection):
        self.prize = prize
        self.selection = selection
    def test(self, switch):
        if self.selection == self.prize:
            return not switch
        else:
            return switch

if __name__ == '__main__':
    if len(sys.argv) > 1:
        doors = int(sys.argv[1])
    else:
        doors = 3
    winsSwitch = 0
    winsNoSwitch = 0
    
    for prize in range(doors):
        for selection in range(doors):
            game = MontyHall(prize, selection)
            if game.test(True):
                winsSwitch += 1
            if game.test(False):
                winsNoSwitch += 1
    
    print("Antal möjliga kombinationer:", doors ** 2)
    print("Vinster vid byte:", winsSwitch)
    print("Vinster utan byte:", winsNoSwitch)
    print("Sannolikhet för vinst vid byte:", Fraction(winsSwitch, doors ** 2))

