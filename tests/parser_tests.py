import unittest
from event_parser import EventParser
import re
import datetime

class TestStory(unittest.TestCase):

    new_story_xml = """<?xml version="1.0" encoding="UTF-8"?>
                        <activity>
                          <id type="integer">38053317</id>
                          <version type="integer">2</version>
                          <event_type>story_create</event_type>
                          <occurred_at type="datetime">2010/11/27 12:41:20 UTC</occurred_at>
                          <author>Grant Klopper</author>
                          <project_id type="integer">153301</project_id>
                          <description>Grant Klopper added &quot;This is the title&quot;</description>
                          <stories>
                            <story>
                              <id type="integer">6798545</id>
                              <url>http://www.pivotaltracker.com/services/v3/projects/153301/stories/6798545</url>
                              <name>This is the title</name>
                              <story_type>feature</story_type>
                              <description>Please add something here</description>
                              <current_state>unscheduled</current_state>
                            </story>
                          </stories>
                        </activity>"""

    accepted_story_xml = """<?xml version="1.0" encoding="UTF-8"?>
                        <activity>
                          <id type="integer">38091177</id>
                          <version type="integer">12</version>
                          <event_type>story_update</event_type>
                          <occurred_at type="datetime">2010/11/28 06:53:04 UTC</occurred_at>
                          <author>Grant Klopper</author>
                          <project_id type="integer">153301</project_id>
                          <description>Grant Klopper accepted &quot;One more for luck&quot;</description>
                          <stories>
                            <story>
                              <id type="integer">6799253</id>
                              <url>http://www.pivotaltracker.com/services/v3/projects/153301/stories/6799253</url>
                              <accepted_at type="datetime">2010/11/28 06:53:04 UTC</accepted_at>
                              <current_state>accepted</current_state>
                            </story>
                          </stories>
                        </activity>"""

    def test_should_parse_new_story(self):
        event = EventParser().parse(self.new_story_xml)
        self.assertTrue(event.is_create_story_event())
        self.assertFalse(event.is_accept_story_event())
        self.assertEqual(event.story_id, '6798545')
        self.assertEqual(event.story_title, 'This is the title')
        self.assertEqual(event.story_type, 'feature')

    def test_should_parse_accepted_story(self):
        expected_date = datetime.date(2010, 11, 28)
        event = EventParser().parse(self.accepted_story_xml)
        self.assertTrue(event.is_accept_story_event())
        self.assertFalse(event.is_create_story_event())
        self.assertEqual(event.story_id, '6799253')
        self.assertEqual(event.accepted_date, expected_date)
