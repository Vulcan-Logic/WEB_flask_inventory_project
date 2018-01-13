import webapp2

from welcomeHandler import welcomeHandler
from productsHandler import addProductsHandler
from productsHandler import listProductsHandler
from productsHandler import skuHandler
from typeHandler import *


app = (webapp2.WSGIApplication([('/', welcomeHandler),
                                ('/addInitialTypes',initialAddtype),
                                ('/products/getTypeList',getTypeList),
                                ('/products/add',addProductsHandler),
                                ('/products/list',listProductsHandler),
                                ('/products/sku',skuHandler),
                                ('/products/checkDesc',validateTypeDesc),
                                ('/products/checkCode',validateTypeCode),
                                ('/products/insertType',insertType),
                                ('/starterTest', getStarterTypes),
                                ('/getStarterTypesJSON', 
                                                    getStarterTypesJSON)], 
                               debug = True))

