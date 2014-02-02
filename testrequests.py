from google.appengine.api import users
import webapp2
import jinja2
import os
import requests
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),
    extensions=['jinja2.ext.autoescape'])

  
# A helper to do the rendering and to add the necessary
# variables for the _base.htm template
def doRender(handler, tname = 'index.htm', template_values = { }):
  template = JINJA_ENVIRONMENT.get_template(tname)
  # Make a copy of the dictionary and add the path and session
  newval = dict(template_values)
  #handler.session = Session()
  #if 'username' in handler.session:
     #newval['username'] = handler.session['username']
  handler.response.write(template.render(newval))
  return True

class Response(object):
	status = 0;
	tomatosdata = ""
	mapdata = ""
	imdbdata = ""
	youtube = ""
	top10 = ""

class ErrorResponse(object):
	status = 301
	text = "No search term"
	
class search(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
	search_term = self.request.get('s');
	
	if search_term:
		response = Response()
		response.status = 200

		r = requests.get('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=dz92w5jph4fdf723894jydan&q=' + search_term + '&page_limit=1')
		response.tomatosdata = r.json()

		//r1 = requests.get('http://www.omdbapi.com/?s=' + search_term)
//		response.imdbdata = r1.json()

		r2 = requests.get('http://gdata.youtube.com/feeds/api/videos?q=' + search_term + ' trailer&alt=json&key=AI39si6yd23pxhzYn5BxyV_Tl1I5aCUDwDG7Xh7DhLYQej1L7h_rTjHyNvVoguGrBLx_X6QqTKpvuQ2lECfP-3YuoIY_O5ctEg')
		response.youtube = r2.json();

	else:
		response = ErrorResponse()
		response.status = 301
		response.text = "No search term"

	r3 = requests.get('http://api.rottentomatoes.com/api/public/v1.0/lists/movies/box_office.json?apikey=dz92w5jph4fdf723894jydan&limit=10&country=uk');
	response.top10 = r3.json();
		

        if user:
		logout_url = users.create_logout_url(self.request.path)
        	template_values = {
		    'user': user.nickname(),
		    'url_logout': logout_url,
		    'url_logout_text': 'Log out',
		    'search_term':search_term,
		    'results':response
        	}
		doRender(self,'index.html',template_values)
        else:
            self.redirect(users.create_login_url(self.request.uri))


application = webapp2.WSGIApplication([
    ('/', search),
], debug=True)
