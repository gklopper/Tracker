import unittest
from models import Story
from models import StoryLine
from datetime import date

class TestStory(unittest.TestCase):
    
    def test_actual_java_days(self):
        story = StoryStub(name='foo', story_id='bar')
        actual_java_days = story.actual_java_days()
        self.assertAlmostEqual(actual_java_days, 1.571, 3)


    def test_actual_cs_days(self):
        story = StoryStub(name='foo', story_id='bar')
        actual_cs_days = story.actual_cs_days()
        self.assertAlmostEqual(actual_cs_days, 2.714, 3)

class StoryStub(Story):
    def story_lines(self):
        return [StoryLine(java_hours = 5, cs_hours = 3, story_id = 'bar', date= date.today()),
                StoryLine(java_hours = 2, cs_hours = 7, story_id = 'bar', date= date.today()),
                StoryLine(java_hours = 4, cs_hours = 9, story_id = 'bar', date= date.today())]