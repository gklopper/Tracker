from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from models import Story, Project
import logging
from event_parser import EventParser
import os



class Handler(webapp.RequestHandler):



    def _create_new_story(self, event):
        logging.info('Creating story')
        story = Story(story_id=event.story_id, name=event.story_title)
        story.put()

        project = Project.get()

        api_url = 'http://www.pivotaltracker.com/services/v3/projects/{PROJECT_ID}/stories/{STORY_ID}/notes'.replace('{PROJECT_ID}', project.project_id).replace('{STORY_ID}', story.story_id)
        comment_xml = '<note><text>http://{APP_ID}.appspot.com/s/{STORY_ID}</text></note>'.replace('{APP_ID}', os.environ['APPLICATION_ID']).replace('{STORY_ID}', story.story_id)

        logging.info('Api url: ' + api_url)
        logging.info('Comment xml: ' + comment_xml)

        #post a comment back to pivotal tracker
        result = urlfetch.fetch(url=api_url,
                                payload=comment_xml,
                                method=urlfetch.POST,
                                headers={'Content-Type': 'application/xml', 'X-TrackerToken': project.api_token})
        logging.info('Result of API call: ' + result.content)

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