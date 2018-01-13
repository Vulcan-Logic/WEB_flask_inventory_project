from templating import Handler1
from dbProduct import ProductQuery
from dbProductType import TypeQuery

class addProductsHandler(Handler1):
	def get(self):
		# check authentication before displaying page.
		self.display()
			
	def display(self,user=""):
		sData=TypeQuery().getTypesByParentId(0)
		if (sData is not None) or (sData != 0):
			self.render("ap.html",sData=sData,cont=True)
		else:
			self.render("ap.html",cont=False)
			
	def post(self):
		print("post called with data")
		
	
class listProductsHandler(Handler1):
	def get(self):
		message=None
		products=ProductQuery().getAllProducts()
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
		pKey=self.request.get('product')
		#print("product key in urlsafe mode :")
		#print(pKey)
		if pKey.strip() != "":
			product=ProductQuery().getProduct(key=pKey)
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
	
	
	
	
	
	
	
	
	
	