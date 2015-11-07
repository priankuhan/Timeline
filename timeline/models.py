from couchdbkit.ext.django.schema import *
from datetime import datetime
from django.db import models

class Uploader(models.Model):
    docfile = models.FileField(upload_to='media')

class Item(Document):
    author = StringProperty()
    content = StringProperty(required=True)
    date = DateTimeProperty(default=datetime.utcnow)