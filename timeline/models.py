from couchdbkit.ext.django.schema import *
from datetime import datetime


class Item(Document):
    author = StringProperty()
    content = StringProperty(required=True)
    date = DateTimeProperty(default=datetime.utcnow)