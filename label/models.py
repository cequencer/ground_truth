from django.db import models

class Label(models.Model):
    label_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=100)
    label_source = models.IntegerField()

    def __unicode__(self):
        return self.label

    def __eq__(self, other):
        return self.label == other.label