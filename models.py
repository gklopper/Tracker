from google.appengine.ext import db

class Story(db.Model):
    story_id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    user = db.UserProperty()
    java_estimate = db.IntegerProperty(default=0, required=True)
    cs_estimate = db.IntegerProperty(default=0, required=True)
    last_updated = db.DateProperty()

    def story_lines(self):
        return StoryLine.gql('WHERE ANCESTOR IS :story ORDER BY date', story=self).fetch(100, 0)

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

