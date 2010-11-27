from xml.dom import minidom

class Event(object):
    event_type = None
    story_type = None
    id = None
    title = None

    def is_create_story_event(self):
        return self.event_type == 'story_create' and self.story_type == 'feature'

class EventParser:

    def parse(self, xml_string):
        event_xml = minidom.parseString(xml_string)
        event = Event()
        event.event_type = event_xml.getElementsByTagName('event_type')[0].firstChild.nodeValue

        if event.event_type == 'story_create':
            story_xml = event_xml.getElementsByTagName("story")[0]
            event.id = story_xml.getElementsByTagName('id')[0].firstChild.nodeValue
            event.title = story_xml.getElementsByTagName('name')[0].firstChild.nodeValue
            event.story_type = story_xml.getElementsByTagName('story_type')[0].firstChild.nodeValue

        return event
        