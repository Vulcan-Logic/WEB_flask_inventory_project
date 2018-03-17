from google.appengine.ext import ndb
from dbProductType import TypeQuery
import logging


#the parent key of this should be product
class ProductField(ndb.Model):
	fieldName = ndb.StringProperty() #product field description
	fieldValue=ndb.StringProperty() #product field contents
	
	def get(self, parentKey=None):
		pass
	
	def set(self, parentKey=None, fName=None, fCont=None):
		#set product field names and values
		pass

#the parent key of this should be product
class ProductImages(ndb.Model):
	imageName=ndb.StringProperty()
	imageLocation=ndb.StringProperty()
	def get(self,parentKey=None):
		pass
	
	def set(self,parentKey=None, iName=None, iLocatn=None):
		#set the image name and location url
		pass

class Product(ndb.Model):
	pName = ndb.StringProperty(required=True) #product name
	pFields=ndb.StructuredProperty(ProductField,repeated=True)
	pImages=ndb.StructuredProperty(ProductImages,repeated=True)
	reqSKU=ndb.StringProperty()
	SKU=ndb.StringProperty()
	#Active, Retired, Inactive
	pStatus=ndb.StringProperty()
	dateCreated=ndb.DateTimeProperty(auto_now_add=True)
	dateModified=ndb.DateTimeProperty(auto_now=True)
	modifiedBy=ndb.KeyProperty()

class ProductQuery():
	def get(self):
		#will send back all products in file. 
		pQuery=Product().query()
		if pQuery.count()>0:
			return(pQuery.fetch())
		else:
			return(None)

#add a product 	
	@ndb.transactional(xg=True)
	def put(self,pKey,pName,pSku,prodDesc,pFieldList,pImageList,\
		modifiedBy):
		#start a transaction here 
		# to start with add the product fields yourself.
		#get generated SKU from the database
		try:
			baseSKU=pSku.rsplit('-',1)[0]
			counter=TypeQuery().setTypeCounterByKey(key=pKey)
			SKU=baseSKU+str(counter)
			parentKey=ndb.Key(urlsafe=pKey)
			entry = (Product(pName = pName, pFields=pFieldList,\
			pImages=pImageList,\
			reqSKU=pSku,SKU=SKU,pStatus="Active",modifiedBy=modifiedBy,\
			parent=parentKey))
			if entry.put() is not None: 
				retString=("Inserted Product, requested SKU:"+pSku+\
				" SKU:" +SKU)
				return(retString)
			else:
				raise Exception(500, "Unable to add product to db")
		except Exception as e:
				logging.exception(e)
				raise e
			
#get product details via sku or key
	def getProduct(self,sku=None,key=None):
		if sku is not None:
			query=self.query(Product.sku==sku)
			if query.count()>0:
				return(query.fetch())
			else:
				return(None)
		elif key is not None:
			key=ndb.Key(urlsafe=key)
			query=self.query(Product.key == key)
			if query.count()>0:
				return(query.fetch())
			else:
				return(None)
		
	def getProductsByName(self,name=None):
		if name is not None:
			query=self.query(Product.pName == name)
			if query.count()>0:
				return(query.fetch())
			else:
				return(None)
		else:
			return(None)
	
	def getProductsByType(self,pType=None):
		if  pType is not None:
			query=self.query(Product.pType == pType)
			if query.count()>0:
				return(query.fetch())
			else:
				return(None)
		else:
			return(None)
	

		
		
		