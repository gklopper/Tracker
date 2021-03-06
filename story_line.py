from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import users
from models import Story, StoryLine

import datetime
import re
import appengineutils
import logging


def last_five_days():
        today = datetime.date.today()
        date_list = []
        for x in range(0, 5):
            date_list.append(today - datetime.timedelta(days = x))
        return date_list

class DeleteHandler(webapp.RequestHandler):

    def get(self, story_id, line_id):
        story = Story.get_by_story_id(story_id)
        story_line = StoryLine.get_by_id(int(line_id), parent=story)
        story_line.is_deleted = True
        story_line.deleted_by_user = users.get_current_user()
        story_line.put()

        self.redirect('/s/' + story_id)


class Handler(webapp.RequestHandler):

    def post(self, story_id):

        story = Story.get_by_story_id(story_id)

        date_match = re.search(r'(\d\d\d\d)-(\d\d)-(\d\d)', self.request.get('date'))
        year = int(date_match.group(1))
        month = int(date_match.group(2))
        day = int(date_match.group(3))
        date = datetime.date(year, month, day)
        java_hours = int(self.request.get('java_hours'))
        cs_hours = int(self.request.get('cs_hours'))
        comment = self.request.get('comment')
        
        story_line = StoryLine(story_id=story_id,
                               comment=comment,
                               date=date,
                               user=users.get_current_user(),
                               java_hours=java_hours,
                               cs_hours=cs_hours,
                               parent=story)
        
        story_line.put()
        story.last_updated = story_line.date
        story.put()

        java_days = story.actual_java_days()
        cs_days = story.actual_cs_days()

        if story.java_estimate > 0 and story.java_estimate < java_days:
            logging.warn("Over java estimate")

        if story.cs_estimate > 0 and story.cs_estimate < cs_days:
            logging.warn("Over cs estimate")


        self.redirect('/s/' + story_id)

    def get(self, story_id):

        story = Story.get_by_story_id(story_id)

        if story is None:
            logging.info('creating story ' + story_id)
            story = Story(story_id=story_id, user = users.get_current_user(), name=story_id)
            story.put()

        story_lines = story.story_lines()

        java_days = story.actual_java_days()
        cs_days = story.actual_cs_days()

        appengineutils.render_template(self.response, 'story_history.html', {'story_lines': story_lines,
                                                                'dates': last_five_days(),
                                                                'java_days': java_days,
                                                                'cs_days': cs_days,
                                                                'story': story})

def main():
    application = webapp.WSGIApplication([('/s/(.*)/(.*)/delete', DeleteHandler),
                                          ('/s/(.*)', Handler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
