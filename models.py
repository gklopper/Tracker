from google.appengine.ext import db

class Story(db.Model):
    story_id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    user = db.UserProperty()
    java_estimate = db.IntegerProperty(default=0, required=True)
    cs_estimate = db.IntegerProperty(default=0, required=True)
    last_updated = db.DateProperty()

    _story_lines = None

    def story_lines(self):
        if self._story_lines is None:
            self._story_lines = StoryLine.gql('WHERE ANCESTOR IS :story ORDER BY date', story=self).fetch(100, 0)
        return self._story_lines

    def actual_java_days(self):
        total_java_hours = 0

        for story_line in self.story_lines():
            if not story_line.is_deleted:
                total_java_hours += story_line.java_hours

        java_days = float(total_java_hours) / 7
        return java_days

    def actual_cs_days(self):
        total_cs_hours = 0

        for story_line in self.story_lines():
            if not story_line.is_deleted:
                total_cs_hours += story_line.cs_hours

        cs_days = float(total_cs_hours) / 7
        return cs_days

    @classmethod
    def get_by_story_id(cls, story_id):
        return Story.gql('WHERE story_id = :story_id', story_id=story_id).get()


class StoryLine(db.Model):
    story_id = db.StringProperty(required=True)
    date = db.DateProperty(required=True)
    comment = db.StringProperty()
    user = db.UserProperty()
    java_hours = db.IntegerProperty(required=True)
    cs_hours = db.IntegerProperty(required=True)
    is_deleted = db.BooleanProperty(required=True, default=False)
    deleted_by_user = db.UserProperty()

