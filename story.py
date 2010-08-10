from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import util
import appengineutils


from google.appengine.api import users

class Story(db.Model):
    story_id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    user = db.UserProperty()
    java_estimate = db.IntegerProperty(default=0, required=True)
    cs_estimate = db.IntegerProperty(default=0, required=True)


class Handler(webapp.RequestHandler):

    def get(self, story_id):

        story = Story.gql('WHERE story_id = :1', story_id).get()

        appengineutils.render_template(self.response, 'story.html', {"story" : story})


def main():
    application = webapp.WSGIApplication([('/p/(.*)', Handler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()