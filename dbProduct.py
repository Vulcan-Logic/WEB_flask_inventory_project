from google.appengine.ext import ndb

class ProductField(ndb.Model):
	fieldName = ndb.StringProperty() #product field description
	fieldContents=ndb.StringProperty() #product field contents

class Product(ndb.Model):
	pType=ndb.IntegerProperty() #product type
	pName = ndb.StringProperty(required=True) #product name
	pField=ndb.StructuredProperty(ProductField,repeated=True)
	dateCreated=ndb.DateTimeProperty(auto_now_add=True)
	dateModified=ndb.DateTimeProperty(auto_now=True)
	modifiedBy=ndb.KeyProperty()
	
	
class ProductQuery():
	
	def getAllProducts(self):
		pQuery=Product.query()
		if pQuery.count()>0:
			return(pQuery.fetch())
		else:
			return(None)

#add a product 	
	def addProduct(self,pType,pName):
		#start a transaction here 
		# to start with add the product fields yourself.
		tField=None
		entry = (Product(pType = pType,pName = pName,pField = tField))
		return(entry.put())

#get product details via sku or key
	def getProduct(self,sku=None,key=None):
		if sku is not None:
			query=Product.query(Product.sku==sku)
			if query.count()>0:
				return(query.fetch())
			else:
				return(None)
		elif key is not None:
			key=ndb.Key(urlsafe=key)
			query=Product.query(Product.key == key)
			if query.count()>0:
				return(query.fetch())
			else:
				return(None)
		
	def getProductsByName(self,name=None):
		if name is not None:
			query=Product.query(Product.pName == name)
			if query.count()>0:
				return(query.fetch())
			else:
				return(None)
		else:
			return(None)
	
	def getProductsByType(self,pType=None):
		if  pType is not None:
			query=Product.query(Product.pType == pType)
			if query.count()>0:
				return(query.fetch())
			else:
				return(None)
		else:
			return(None)
	

		
		
		