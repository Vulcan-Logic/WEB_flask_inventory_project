import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
jinja_env2 = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = False)
        
class Handler1(webapp2.RequestHandler):
    def write(self,*a, **s):
        self.response.out.write(*a,**s)

    def render_str(self,template,**parameters):
        t = jinja_env.get_template(template)
        return t.render(parameters)
        
    def render(self,template,**params):
        self.write(self.render_str(template, **params))
        
class Handler2(webapp2.RequestHandler):
    def write(self,*a, **s):
        self.response.out.write(*a,**s)

    def render_str(self,template,**parameters):
        t = jinja_env2.get_template(template)
        return t.render(parameters)
        
    def render(self,template,**params):
        self.write(self.render_str(template, **params))
        