'''
Created on 15-Dec-2017

@author: vineet
'''

from google.appengine.ext import ndb

class ProductInventory(ndb.Model):
    sku = ndb.StringProperty() #product sku
    site = ndb.StringProperty() #site where it is stored
    qtyStock=ndb.FloatProperty()
    qtyAv = ndb.FloatProperty() #available quantity
    sPrice = ndb.FloatProperty()
    dateCreated = ndb.DateTimeProperty(auto_now_add=True)
    dateModified = ndb.DateTimeProperty(auto_now=True)
    
