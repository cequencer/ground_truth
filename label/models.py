from django.db import models

class Label(models.Model):
    label_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=100)

    def __unicode__(self):
        return self.label
