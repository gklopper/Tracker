from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util
from models import Story

import appengineutils

class Handler(webapp.RequestHandler):

    def get(self):
        stories = db.GqlQuery("SELECT * FROM Story ORDER BY last_updated DESC").fetch(1000, 0)    
        appengineutils.render_template(self.response, 'report.html', {"stories" : stories})



def main():
    application = webapp.WSGIApplication([('/report', Handler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()