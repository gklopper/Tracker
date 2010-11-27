from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from xml.dom import minidom
from models import Story
import logging
from event_parser import EventParser


class Handler(webapp.RequestHandler):
    event_parser = EventParser()

    def post(self):
        logging.info('Received event from Pivotal Tracker')
        event_xml = self.request.body
        logging.info('Event xml: ' + event_xml)
        event = self.event_parser.parse(event_xml)
        logging.info('Parsed event: ' + str(event))
        if event.is_create_story_event:
            logging.info('Creating story')
            story = Story(story_id = event.id, name = event.title, )
            story.put()

def main():
    application = webapp.WSGIApplication([('/pivotaltracker', Handler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()