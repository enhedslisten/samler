from peewee import *

db = SqliteDatabase('db.sqlite3')

class Posts(Model):
    orig_post_id = IntegerField()
    orig_user_id = IntegerField()
    date = IntegerField()
    username = CharField()
    text = CharField(null=True)
    image_small = CharField(null=True)
    image_full = CharField(null=True)
    service = CharField(null=True)
    likes = IntegerField(null=True)
    orig_url = CharField(null=True)
    hidden = BooleanField(null=False)
    promoted = BooleanField(null=False)

    def hasPost(self, id):
        return Posts.select().where(Posts.orig_post_id == id).count()

    def highID(self, service):
        post =  Posts.select(Posts.orig_post_id).where(Posts.service==service).order_by(Posts.orig_post_id.desc()).limit(1).first()
        if post:
            return post.orig_post_id
        else:
            return False

    class Meta:
        database = db
