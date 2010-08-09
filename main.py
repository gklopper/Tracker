from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
import datetime
import logging

import os

def last_five_days():
        today = datetime.date.today()
        date_list = []
        for x in range(0, 5):
            date_list.append(today - datetime.timedelta(days = x))
        logging.info(date_list)
        return date_list

class StoryLine(db.Model):
    story_id = db.StringProperty(required=True)
    date = db.DateProperty(required=True)
    comment = db.StringProperty()
    user = db.UserProperty()


class StoryHandler(webapp.RequestHandler):

    def post(self, story_id):
        story = new StoryLine()

    def get(self, story_id):
        stories = StoryLine.gql('WHERE story_id = :1 ORDER BY date', story_id).fetch(100, 0)
        last_five_days()
        template_values = {
            'stories': stories,
            'story_id': story_id,
            'dates': last_five_days()
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/story_history.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/admin/story/(.*)', StoryHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
