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

def compute_file_path(instance, filename):
    if instance.prediction_source == 1:
        filename += '.stanfordner'
    else:
        filename += '.crfsuite'
    
    return os.path.join(UPLOAD_ROOT, filename)


class PredictionFile(models.Model):
    prediction_file_id = models.AutoField(primary_key=True)
    researcher = models.CharField(max_length=100)
    # stanfordner_tagged = models.FileField(upload_to=get_file_path_stanfordner)
    # crfsuite_tagged = models.FileField(upload_to=get_file_path_crfsuite)
    tagged_file = models.FileField(upload_to=compute_file_path)
    prediction_source = models.IntegerField()   #1: stanfordner, 2: crfsuite
    version = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.researcher

    def get_path(self):
        return MEDIA_ROOT + str(self.tagged_file)
    # def get_path_stanfordner(self):
    #     return MEDIA_ROOT + str(self.stanfordner_tagged)

    # def get_path_crfsuite(self):
    #     return MEDIA_ROOT + str(self.crfsuite_tagged)

    def save(self):
        curr_version_no = 0
        if PredictionFile.objects.filter(researcher=self.researcher, prediction_source=self.prediction_source).exists():   #update version
            prev_version_no = PredictionFile.objects.filter(researcher=self.researcher)[0].version
            curr_version_no = prev_version_no + 1

        self.version = curr_version_no
        super(PredictionFile, self).save()
