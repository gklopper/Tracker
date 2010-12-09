from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util
from models import Story

import appengineutils
import datetime
import logging

class LatestUpdatesReport(webapp.RequestHandler):

    def get(self):
        stories = db.GqlQuery("SELECT * FROM Story ORDER BY last_updated DESC").fetch(50, 0)    
        appengineutils.render_template(self.response, 'report.html', {'stories' : stories, 'period' : 'Latest updates'})

class MonthReport(webapp.RequestHandler):

    def get(self, _year, _month):

        logging.info('Running report for: ' + _year + '/' + _month)

        year = int(_year)
        month = int(_month)

        next_month = month + 1

        this_month = datetime.date(year, month, 1)

        if (next_month == 13):
            next_month = 1
            year = year + 1

        next_month = datetime.date(year, next_month, 1)

        logging.info('this_month: ' + str(this_month))
        logging.info('next_month: ' + str(next_month))

        stories = db.GqlQuery("""SELECT * FROM Story
                                    WHERE date_accepted >= :this_month AND date_accepted < :next_month
                                    ORDER BY date_accepted ASC""", this_month=this_month, next_month=next_month).fetch(1000, 0)

        appengineutils.render_template(self.response, 'report.html', {'stories' : stories, 'period' : this_month.strftime("%B %Y")})


def main():
    application = webapp.WSGIApplication([('/report', LatestUpdatesReport),
                                          ('/report/(.*)/(.*)', MonthReport)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()