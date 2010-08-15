from google.appengine.ext import webapp

from google.appengine.ext.webapp import util
import appengineutils
from google.appengine.api import users
from models import StoryLine

class Handler(webapp.RequestHandler):

    def get(self, story_id):



        appengineutils.render_template(self.response, 'report.html', {"stories" : stories})



def main():
    application = webapp.WSGIApplication([('/report', Handler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()