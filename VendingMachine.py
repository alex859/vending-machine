# -*- coding: utf-8 -*-
'''
Created on 04/dic/2013

@author: alex859
'''
from Product import Product
from Coin import Coin

def format_money(amount):
    return '£ '+'{:4.2f}'.format(amount)

class VendingMachine:
    '''
    A vending machine that can be loaded with coins and products, can receive money and give back a product
    and the change if necessary
    '''


    def __init__(self, products, coins):
        '''Initialize the state of the machine that is given by products, coins, credit and balance'''
        self.products={}
        '''A dictonary containing the products'''
        
        self.coins={}
        '''Different coins useful to give change'''
        
        self.credit=0
        '''Holds the amount that the machine holds if it cannot give the change'''
        
        self.balance=0
        '''The amount earned by the machine'''
        
        self.coin_types=['£2','£1','50p','20p','10p','5p','2p','1p']
        '''We use this list to have an order of coins when we compute the change'''
        
        #Initialize the machine
        self.reload(products, coins)
        
    def reload(self, products, coins):
        '''Reloads the machine with the given products and coins'''
        #Start loading the products
        for p in products:
            #if the product is not present create a new one
            current_product=self.products.get(p.code,Product('', '', 0, 0))
            #update name, code and price
            current_product.name=p.name
            current_product.code=p.code
            current_product.price=p.price
            #add the new items
            current_product.quantity=current_product.quantity+p.quantity
            #update the dictionary
            self.products[p.code]=current_product
        #Continue loading the coins
        for c in coins:
            #if the coin is not present create a new one
            current_coin=self.coins.get(c.type,Coin(c.type, c.value, 0))
            #type and value are constant here
            #add the new coins
            current_coin.quantity=current_coin.quantity+c.quantity
            #update the dictionary
            self.coins[c.type]=current_coin
            
    def show_products(self):
        '''Show products with their code and price'''
        for p in self.products.values():
            print str(p.code) + '- '+p.name+': '+format_money(p.price)
    
    def show_credit(self):
        '''Show the available credit'''
        print 'Credit: '+ format_money(self.credit)
        
    def show_status(self):
        '''Shows the status (that is products, coins and balance of the machine)'''
        print 'Balance: '+format_money(self.balance)+'\n'
        print 'Products:'
        for p in self.products.values():
            print p.name+': '+'{:4.0f}'.format(p.quantity)+' items'
        print '\n'
        for c in self.coins.values():
            print '{0: <4}'.format(c.type) + '{:4.0f}'.format(c.quantity)+' items'
    
    def give_product(self,code,money):
        '''Respond to a user that asks for the product with the given code inserting the given money'''
        try:
            p=self.products[code]
            #first of all check if the product is present
            if p.quantity>0:
                #we check if the money inserted plus the credit is enough
                if p.price<=(money+self.credit):
                    #ok we can give the product
                    result={'product':p.name}
                    p.quantity=p.quantity-1
                    change=money-p.price
                    given_change=0
                    if change>0:
                        given_change=self.compute_given_change(self.coin_types,change)
                    result['change']=given_change
                    result['message']='OK'
                    self.balance=self.balance+p.price
                    if change>given_change:
                        self.credit=self.credit+change-given_change
                    return result
                else:
                    return {'message':'Not enough money', 'product':None}
            else:
                return {'message':'Product not present', 'product':None}
        except KeyError:
            return {'message':'Invalid code', 'product':None}
        
    def compute_given_change(self, coin_types, change):
        '''Compute the change that the machine can give on the base of the coins it has'''
        given_change=0
        for coin_type in coin_types:
            try:
                c=self.coins[coin_type]
                if c.value>change or c.quantity==0:
                    return self.compute_given_change(coin_types[1:], change)
                else:
                    #how many coins are needed
                    needed_coin_num=change/c.value
                    given_coins=0
                    if needed_coin_num<=c.quantity:
                        given_coins=needed_coin_num
                    else:
                        #we give all the coins
                        given_coins=c.quantity
                    #compute the given change at this step
                    given_change=given_coins*c.value
                    #update the number of coins
                    c.quantity=c.quantity-given_coins
                    #do we need extra change?
                    extra_change=change-given_change
                    if extra_change>0:
                        return given_change+self.compute_given_change(coin_types[1:], extra_change)
                    else:
                        return given_change
            #if that type of coin is not present
            except KeyError:
                return self.compute_given_change(coin_types[1:], change)
        return given_change        
          
            
    