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

        appengineutils.render_template(self.response, 'story.html', {"story" : story,
                                                                      "estimate_options": [0,1,2,3,4,5,6,7,8,9,10]})

    def post(self, story_id):
        story = Story.gql('WHERE story_id = :1', story_id).get()
        story.name = self.request.get('name')
        story.java_estimate = int(self.request.get('java_estimate'))
        story.cs_estimate = int(self.request.get('cs_estimate'))

        story.user = users.get_current_user()

        story.save()
        self.redirect('/s/' + story.story_id)


def main():
    application = webapp.WSGIApplication([('/p/(.*)', Handler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()