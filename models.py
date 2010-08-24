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

    def _hour_total(self): return lambda total, hours: total + hours

    def actual_java_days(self):
        return reduce(self._hour_total(),
                      map(lambda line: float(line.java_hours), self.story_lines())) / 7

    def actual_cs_days(self):
        return reduce(self._hour_total(),
                      map(lambda line: float(line.cs_hours), self.story_lines())) / 7

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

