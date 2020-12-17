# import * means import everything from peewee

from peewee import *
from peewee import TextField
from playhouse.postgres_ext import ArrayField
import datetime, os, urllib.parse
from flask_login import UserMixin

#import sample
# Connect to a Postgres database.
if "DATABASE_URL" in os.environ:
    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    DATABASE = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
else:
    DATABASE = PostgresqlDatabase('flask_bookshelf_app', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = DATABASE

class User(UserMixin, BaseModel):
    id = AutoField()
    username = CharField(unique=True)
    fullname = CharField(null=True)
    email = CharField(index=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False) 


class Book(BaseModel):
    book_id = CharField(null=True)
    olid=CharField(null=True, unique=True)
    user = ForeignKeyField(User, backref='books')
    title = CharField(null=True)
    subtitle = CharField(null=False)
    author=CharField()
    requested_by = ArrayField(IntegerField)
    lend_to = IntegerField(default=None, null=True)
    image = CharField(max_length=150, null=True)
    created_at = DateTimeField(default=datetime.datetime.now)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Book], safe=True)
    print("TABLES Created")
    DATABASE.close()