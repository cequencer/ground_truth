from django.db import models
from ground_truth.settings import MEDIA_ROOT
import datetime
import os

UPLOAD_ROOT = 'pubs'

class Pubfile(models.Model):
    pubfile_id = models.AutoField(primary_key=True)
    pubfile_name = models.CharField(max_length=100, unique=True)
    pubfile_file = models.FileField(upload_to=UPLOAD_ROOT)

    def __unicode__(self):
        return self.pubfile_name

    def get_path(self):
        return MEDIA_ROOT + str(self.pubfile_file)