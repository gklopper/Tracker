from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from xml.dom import minidom
from models import Story
import logging


class Handler(webapp.RequestHandler):



    def post(self):

        update_xml = minidom.parseString(self.request.get('body'))

        if self.is_new_story(update_xml):
            self.create_new(update_xml)

    def create_new(self, updateXml):

        story_xml = updateXml.getElementsByTagName('stories')[0].getElementsByTagName('story')[0]
        story_id = story_xml.getElementsByTagName('id')[0].firstChild.nodeValue
        story_name = story_xml.getElementsByTagName('name')[0].firstChild.nodeValue
        story_type = story_xml.getElementsByTagName('story_type')[0].firstChild.nodeValue
        if story_type == 'feature' or story_type == 'chore' or story_type == 'bug':
            logging.info('Created story' + story_id + ' : ' + story_name)
            Story(story_id=story_id, name=story_name).put()
        else:
            logging.info('Ignoring story type: ' + story_type + '(' + story_id + ' : ' + story_name + ')')

    def is_new_story(self, update_xml):
        return update_xml.getElementsByTagName('event_type')[0].firstChild.nodeValue == 'story_create'

def main():
    application = webapp.WSGIApplication([('/pivotaltracker', Handler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()