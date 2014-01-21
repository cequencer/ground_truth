from django.db import models
from ground_truth.settings import MEDIA_ROOT
import os

UPLOAD_ROOT = 'tagged/'

def get_file_path_stanfordner(instance, filename):
    ext = filename.split('.')[-1]
    filename += '.stanfordner'
    return os.path.join(UPLOAD_ROOT, filename)

def get_file_path_crfsuite(instance, filename):
    ext = filename.split('.')[-1]
    filename += '.crfsuite'
    return os.path.join(UPLOAD_ROOT, filename)


class Validator(models.Model):
    validator_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    stanfordner_tagged = models.FileField(upload_to=get_file_path_stanfordner)
    crfsuite_tagged = models.FileField(upload_to=get_file_path_crfsuite)

    def __unicode__(self):
        return str(self.name)

    def get_path(self):
        return MEDIA_ROOT + str(self.pubfile)
