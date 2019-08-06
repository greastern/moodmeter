import webapp2
import jinja2
import os

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

from google.appengine.api import users

from google.appengine.ext import ndb

class CssiUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()

#This is the welcome page
class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
        signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
        index = the_jinja_env.get_template('Templates/Welcomepage.html')
        self.response.write(index.render())


    else:
      # If the user isn't logged in...
      login_url = users.create_login_url('/')
      index = the_jinja_env.get_template('Templates/Loginpage.html')
      templatedata ={"login_url":login_url}
      self.response.write(index.render(templatedata))
  def post(self):
      user = users.get_current_user()
      # Create a new CSSI user.
      cssi_user = CssiUser(
          first_name=self.request.get('first_name'),
          last_name=self.request.get('last_name'),
          email=user.nickname())
      # Store that Entity in Datastore.
      cssi_user.put()
      # Show confirmation to the user. Include a link back to the index.
      self.response.write('Thanks for signing up, %s! <br><a href="/">Welcomepage</a>' %
          cssi_user.first_name)

#This is the dpression page
class Depressionpage(webapp2.RequestHandler):
    def get(self):
     welcome_template = the_jinja_env.get_template('moodmeter/Depression.html')
     self.response.write(welcome_template.render())
#This is the WikiPage for Depression
class WikiDepressionPage(webapp2.RequestHandler):
    def get(self):
     welcome_template = the_jinja_env.get_template('moodmeter/WikiPage.html')
     self.response.write(welcome_template.render())





app = webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/Depression', Depressionpage),
        ('/Depressionwiki', WikiDepressionPage)
        

], debug=True)
