import webapp2
import os
import jinja2
from google.appengine.ext import db
import urllib2
import json

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape = True)

class Handler(webapp2.RequestHandler):
  def write(self,*a,**kw):
    self.response.out.write(*a,**kw)
  def render_str(self,template,**params):
    t=jinja_env.get_template(template)
    return t.render(params)
  def render(self,template,**kw):
    self.write(self.render_str(template,**kw))

#----------------------------------------- API -----------------------------------------------#
URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=28.5363455,77.2704164&types=police|hospital|atm|car_repair|&radius=500&key=AIzaSyCYLV4m6V0pywVTu5xvr8OO8O7gy_WjRkY"
def nearbyLocation():
  content = None
  try:
    content = json.loads(urllib2.urlopen(URL).read())
  except URLerror:
    return
  if content:
    return content['results']

class MainPage(Handler):
  def get(self):
    self.render('home1.html')

class AboutHandler(Handler):
  def get(self):
    self.render('about.html')

class SignupHandler(Handler):
  def get(self):
    self.render('login.html')

class CurrentLocationHandler(Handler):
  def get(self):
    self.render('current.html')

class DestinationHandler(Handler):
  def get(self):
    self.render('map.html')

class nearbyHandler(Handler):
  def get(self):
    places=nearbyLocation();
    self.render('nearby.html',places=places)

app = webapp2.WSGIApplication([('/', MainPage),('/about',AboutHandler),('/signup',SignupHandler),('/CurrentLocation',CurrentLocationHandler),('/Destination',DestinationHandler),('/nearby',nearbyHandler)
              ], debug=True)
