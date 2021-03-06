from google.appengine.ext import db

class Project(db.Model):
    project_id = db.StringProperty(required=True, default='CHANGEME')
    api_token = db.StringProperty(required=True, default='CHANGEME')

    @classmethod
    def get(cls):
        return Project.get_or_insert('current_project', project_id='changeme')

class Story(db.Model):
    story_id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    user = db.UserProperty()
    java_estimate = db.IntegerProperty(default=0, required=True)
    cs_estimate = db.IntegerProperty(default=0, required=True)
    last_updated = db.DateProperty()
    date_accepted = db.DateProperty()

    _story_lines = None

    def story_lines(self):
        if self._story_lines is None:
            self._story_lines = StoryLine.gql('WHERE ANCESTOR IS :story ORDER BY date', story=self).fetch(100, 0)
        return self._story_lines

    def _hour_total(self): return lambda total, hours: total + hours

    def _story_lines_not_deleted(self):
        return filter(lambda s_line: s_line.is_deleted == False, self.story_lines())

    def actual_java_days(self):
        hours = [float(line.java_hours) for line in self._story_lines_not_deleted()]
        return reduce(self._hour_total(), hours, 0) / 7

    def actual_cs_days(self):
        hours = [float(line.cs_hours) for line in self._story_lines_not_deleted()]
        return reduce(self._hour_total(), hours, 0) / 7

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

    def get_story(self):
        return Story.get_by_story_id(self.story_id)

