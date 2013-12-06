'''
Created on 04/dic/2013

@author: alex859
'''

class Coin:
    '''
    Models a coin type to be loaded in the vending machine
    '''
    def __init__(self, type, value, quantity):
        self.type=type
        self.value=value
        self.quantity=quantity
        