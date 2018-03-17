from templating import Handler1
from dbProduct import ProductQuery
from dbProductType import TypeQuery
import logging

class addProduct():
	def get(self,user=None):
		sData=TypeQuery().getChildTypesByKey()
		if (sData is not None and len(sData)!=0):
			return(sData)
		else:
			return(None)
	
	def put(self,pKey,pName,pSku,prodDesc,pFieldList,pImageList,
		modifiedBy):
		try:
			retVal=ProductQuery().put(pKey,pName,pSku,prodDesc,\
			pFieldList,	pImageList, modifiedBy)
			#add retVal to admin log file, for now print it out
			print(retVal)
		except Exception as e:
			logging.exception(e)
			raise Exception(500,str(e)) 
	
class listProductsHandler(Handler1):
	def get(self):
		message=None
		products=ProductQuery().get()
		print(products)
		if (products is None):
			message="No Products Found" 
		else: 
			#process all entries to make a new dictionary and pass this 
			# on to the rendering page
			
			for product in products:
				print("url safe key is: ")
				print(product.key.urlsafe())
				
			self.render("list.html", products=products, message=message,
				next_page_token=None)

class skuHandler(Handler1):
	def get(self):
		message=None
		pSku=self.request.get('product')
		#print("product key in urlsafe mode :")
		#print(pKey)
		if pSku.strip() != "":
			product=ProductQuery().getProduct(sku=pSku)
			#print("product 0 is")
			#print(product[0])
			if product is not None:
				self.render("view.html", product=product[0], 
						message=message)
			else:
				self.render("view.html", product=None, 
						message="Product Not Found")
		else:
			#raise an exception
			self.render("view.html", product=None, 
					message="Product Not Found")
	
	
	
	
	
	
	
	
	
	