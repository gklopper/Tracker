from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
import datetime
import logging
import re

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
    hours = db.IntegerProperty(required=True)


class StoryHandler(webapp.RequestHandler):

    def post(self, story_id):

        date_match = re.search(r'(\d\d\d\d)-(\d\d)-(\d\d)', self.request.get('date'))
        year = int(date_match.group(1))
        month = int(date_match.group(2))
        day = int(date_match.group(3))
        date = datetime.date(year, month, day)
        hours = int(self.request.get('hours'))
        comment = self.request.get('comment')
        
        story = StoryLine(story_id=story_id, comment=comment, date=date, user=users.get_current_user(), hours=hours)
        story.save()

        self.redirect('/admin/story/' + story_id)

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
