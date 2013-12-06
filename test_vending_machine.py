# -*- coding: utf-8 -*-
import unittest
from Product import Product
from Coin import Coin
from VendingMachine import VendingMachine

class TestVendingMachine(unittest.TestCase):
    def setUp(self):
        self.products=[]
        self.products.append(Product('P1',1,1.5,10))
        self.products.append(Product('P2',2,0.5,10))
        self.products.append(Product('P3',3,0.3,10))
        self.products.append(Product('P4',4,1,10))
        self.products.append(Product('P5',5,2.5,10))
        self.coins=[]
        self.coins.append(Coin('1p',0.01,10))
        self.coins.append(Coin('2p',0.02,10))
        self.coins.append(Coin('5p',0.05,10))
        self.coins.append(Coin('10p',0.10,10))
        self.coins.append(Coin('20p',0.20,10))
        self.coins.append(Coin('50p',0.50,10))
        self.coins.append(Coin('£1',1,10))
        self.coins.append(Coin('£2',2,10))
                
    def test_reload(self):
        '''Check if the machine contains the loaded products'''
        machine=VendingMachine(self.products,self.coins)
        self.assertEqual(10,machine.products[1].quantity)
        self.assertEqual(10, machine.coins['5p'].quantity)
        machine.reload(self.products,self.coins)
        self.assertEqual(20,machine.products[1].quantity)
        self.assertEqual(20,machine.coins['5p'].quantity)
    
    def test_buy_product_invalid_code(self):
        '''Test if the machine gives no product with appropriate error if a wrong code is typed'''
        machine=VendingMachine(self.products, self.coins)
        result=machine.give_product(10, 100)
        self.assertEqual(None, result['product'])
        self.assertEqual('Invalid code', result['message'])
            
    def test_buy_product_no_product(self):
        '''Test if the machine gives no product if they are finished'''
        machine=VendingMachine([Product('P1',1,1.5,0)],[])
        result=machine.give_product(1, 100)
        self.assertEqual(None, result['product'])
        self.assertEqual('Product not present', result['message'])
        
    def test_buy_product_change_present(self):
        '''Now try to buy a product that is present in the machine, and check that the change is correct'''
        machine=VendingMachine(self.products,self.coins)
        result=machine.give_product(1, 3)
        self.assertEqual('P1', result['product'])
        self.assertEqual(1.5, result['change'])
        
    def test_buy_product_not_enough_money(self):
        '''Now try to buy a product giving less money than needed'''
        machine=VendingMachine(self.products,self.coins)
        result=machine.give_product(1, 0.5)
        self.assertEqual(None, result['product'])
        self.assertEqual('Not enough money', result['message'])
        
    def test_buy_product_not_enough_change(self):
        '''Now try to buy a product but the machine has not enough change'''
        machine=VendingMachine(self.products,[Coin('1p',0.01,10)])
        result=machine.give_product(1, 2)
        self.assertEqual('P1', result['product'])
        self.assertEqual(0.1, result['change'])
        #check the credit on the machine
        self.assertEqual(0.4, machine.credit)
        
    def test_buy_two_products_check_balance(self):
        '''Now try to buy two products cheking at the end if the balance is correct'''
        machine=VendingMachine(self.products,self.coins)
        machine.give_product(1, 3)
        machine.give_product(2, 0.5)
        self.assertEqual(2,machine.balance)
        
    def test_buy_all_products(self):
        '''Now try to buy all the 10 products of type P1. Then try to buy another one'''
        machine=VendingMachine(self.products,self.coins)
        for i in range(10):
            machine.give_product(1, 1.5)
        result=machine.give_product(1, 1.5)
        self.assertEqual(None, result['product'])
        self.assertEqual('Product not present', result['message'])
        
    def test_buy_with_a_lot_of_money(self):
        '''Try to buy a product inserting a lot of money'''
        machine=VendingMachine(self.products,self.coins)
        result=machine.give_product(1, 37.5)
        self.assertEqual('P1', result['product'])
        self.assertEqual(36, result['change'])
        
    def test_buy_with_a_tons_of_money(self):
        '''Try to buy a product inserting more money than the possible change..than free products for all :)'''
        machine=VendingMachine(self.products,self.coins)
        result=machine.give_product(1, 50)
        self.assertEqual('P1', result['product'])
        self.assertEqual(38.8, result['change'])
        #a product given without putting money
        result=machine.give_product(1, 0)
        self.assertEqual('P1', result['product'])
        #but no change!
        self.assertEqual(0, result['change'])

if __name__=='__main__':
    unittest.main()

