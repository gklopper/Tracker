from google.appengine.ext import webapp

from google.appengine.ext.webapp import util
import appengineutils
from google.appengine.api import users
from models import Story

class Handler(webapp.RequestHandler):

    def get(self, story_id):

        story = Story.get_by_story_id(story_id)

        appengineutils.render_template(self.response, 'story.html', {"story" : story,
                                                                      "estimate_options": range(0, 11)})

    def post(self, story_id):
        story = Story.get_by_story_id(story_id)
        story.name = self.request.get('name')
        story.java_estimate = int(self.request.get('java_estimate'))
        story.cs_estimate = int(self.request.get('cs_estimate'))

        story.user = users.get_current_user()

        story.put()
        self.redirect('/s/' + story.story_id)


def main():
    application = webapp.WSGIApplication([('/p/(.*)', Handler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()