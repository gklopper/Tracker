from xml.dom import minidom
import re
import datetime

class Event(object):
    event_type = None
    story_type = None
    story_id = None
    story_title = None
    story_state = None
    accepted_date = None

    def is_create_story_event(self):
        return self.event_type == 'story_create' and self.story_type == 'feature'

    def is_accept_story_event(self):
        return self.event_type == 'story_update' and self.story_state == 'accepted' and self.accepted_date != None

    def is_name_update_event(self):
        return self.story_title != None

    def __str__(self):
        return 'Event[' + self._field(self.event_type, 'event_type') \
            + self._field(self.story_id, 'story_id') \
            + self._field(self.story_state, 'story_state') \
            + self._field(self.story_type, 'story_type') \
            + self._field(self.accepted_date, 'accepted_date') \
            + self._field(self.is_accept_story_event(), 'is_accept_story_event') \
            + self._field(self.is_create_story_event(), 'is_create_story_event') \
            + ']'

    def _field(self, field, name):
        return name + '=' + str(field) + ', '

class EventParser:

    def parse(self, xml_string):
        event_xml = minidom.parseString(xml_string)
        event = Event()
        event.event_type = self._get_text_value_or_none(event_xml, 'event_type')

        if self._is_story_event(event):
            self._handle_story_events(event, event_xml)

        return event

    def _is_story_event(self, event):
        return event.event_type == 'story_create' or event.event_type == 'story_update'

    def _handle_story_events(self, event, event_xml):
        story_xml = event_xml.getElementsByTagName("story")[0]
        event.story_id = self._get_text_value_or_none(story_xml, 'id')
        event.story_title = self._get_text_value_or_none(story_xml, 'name')
        event.story_type = self._get_text_value_or_none(story_xml, 'story_type')
        event.story_state = self._get_text_value_or_none(story_xml, 'current_state')
        if event.story_state == 'accepted':
            event.accepted_date = self._get_date_value_or_none(story_xml, 'accepted_at')

    def _get_text_value_or_none(self, event_xml, field):

        if self._tag_exists(event_xml, field):
            return event_xml.getElementsByTagName(field)[0].firstChild.nodeValue
        else:
            return None

    def _tag_exists(self, event_xml, tag):
        return len(event_xml.getElementsByTagName(tag)) > 0

    def _get_date_value_or_none(self, event_xml, field):
        if self._tag_exists(event_xml, field):
            date_match = re.search(r'(\d\d\d\d)/(\d\d)/(\d\d)', self._get_text_value_or_none(event_xml, field))
            year = int(date_match.group(1))
            month = int(date_match.group(2))
            day = int(date_match.group(3))
            the_date = datetime.date(year, month, day)
            return the_date
        else:
            return None