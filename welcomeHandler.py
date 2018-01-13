from templating import Handler2
from templating import Handler1


class welcomeHandler(Handler2):
	def get(self):
		# check authentication before displaying page.
		self.display()
			
	def display(self,user=""):
		self.render("welcome.html")	
			
