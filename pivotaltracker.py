from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from xml.dom import minidom
from models import Story
import logging
from event_parser import EventParser
import urllib2


class Handler(webapp.RequestHandler):

    def _create_new_story(self, event):
        logging.info('Creating story')
        story = Story(story_id=event.story_id, name=event.story_title, )
        story.put()

        #post a comment back to pivotal tracker


    def _accept_story(self, event):
        logging.info('Accepting story: ' + event.story_id)
        story = Story.get_by_story_id(event.story_id)
        story.date_accepted = event.accepted_date
        story.put()

    def _update_story_name(self, event):
        story = Story.get_by_story_id(event.story_id)
        if story:
            logging.info("Updating story name to: " + event.story_title)
            story.name = event.story_title
            story.put()
        else:
            logging.info("Cannot update story name (" + event.story_id + "): story does not exist")

    def post(self):
        logging.info('Received event from Pivotal Tracker')
        event_xml = self.request.body
        logging.info('Event xml: ' + event_xml)
        event = EventParser().parse(event_xml)

        logging.info(str(event))

        if event.is_create_story_event():
            self._create_new_story(event)
        elif event.is_accept_story_event():
            self._accept_story(event)
        elif event.is_name_update_event():
            self._update_story_name(event)
        else:
            logging.info("Ignoring pivotal tracker update")

def main():
    application = webapp.WSGIApplication([('/pivotaltracker', Handler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()