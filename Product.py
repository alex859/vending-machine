'''
Created on 04/dic/2013

@author: alex859
'''

class Product:
    '''
    Class that models a product type to be loaded in the vending machine
    '''
    def __init__(self, name, code, price, quantity):
        self.name=name
        self.code=code
        self.price=price
        self.quantity=quantity
        