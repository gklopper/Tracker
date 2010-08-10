from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import users
import datetime
import re
import appengineutils
from story import Story


class StoryLine(db.Model):
    story_id = db.StringProperty(required=True)
    date = db.DateProperty(required=True)
    comment = db.StringProperty()
    user = db.UserProperty()
    java_hours = db.IntegerProperty(required=True)
    cs_hours = db.IntegerProperty(required=True)

def last_five_days():
        today = datetime.date.today()
        date_list = []
        for x in range(0, 5):
            date_list.append(today - datetime.timedelta(days = x))
        return date_list



class Handler(webapp.RequestHandler):

    def post(self, story_id):

        date_match = re.search(r'(\d\d\d\d)-(\d\d)-(\d\d)', self.request.get('date'))
        year = int(date_match.group(1))
        month = int(date_match.group(2))
        day = int(date_match.group(3))
        date = datetime.date(year, month, day)
        java_hours = int(self.request.get('java_hours'))
        cs_hours = int(self.request.get('cs_hours'))
        comment = self.request.get('comment')
        
        story_line = StoryLine(story_id=story_id, comment=comment, date=date, user=users.get_current_user(), java_hours=java_hours, cs_hours=cs_hours)
        story_line.save()

        self.redirect('/s/' + story_id)

    def get(self, story_id):

        story = Story.gql('WHERE story_id = :1', story_id).get()

        if story is None:
            story = Story(story_id=story_id, user = users.get_current_user(), name=story_id)
            story.save()

        story_lines = StoryLine.gql('WHERE story_id = :1 ORDER BY date', story_id).fetch(100, 0)

        total_java_hours = 0
        total_cs_hours = 0

        for story_line in story_lines:
            total_java_hours += story_line.java_hours
            total_cs_hours += story_line.cs_hours

        java_days = float(total_java_hours) / 7
        cs_days = float(total_cs_hours) / 7

        appengineutils.render_template(self.response, 'story_history.html', {'stories': story_lines,
                                                                'dates': last_five_days(),
                                                                'total_java_hours': total_java_hours,
                                                                'total_cs_hours' : total_cs_hours,
                                                                'java_days': java_days,
                                                                'cs_days': cs_days,
                                                                'story': story})

def main():
    application = webapp.WSGIApplication([('/s/(.*)', Handler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
