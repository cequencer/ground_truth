from django.db import models
from django.shortcuts import get_object_or_404
from prediction_file.models import PredictionFile
from record.models import Record, Pubtoken
from label.models import Label
from utils.parser import LabeledFileParser
import os

class Validator(models.Model):
    validation_id = models.AutoField(primary_key=True)
    researcher = models.CharField(max_length=100, blank=True)
    prediction_source = models.IntegerField(blank=True, null=True)  
    prediction_file = models.ForeignKey(PredictionFile)

    # class var
    all_labels = Label.objects.all().order_by('label_id')
    LABEL_LOOKUP = {}
    for i in range(3):  #true_label, stanfordner, crfsuite
        for l in all_labels:
            key = '%s-%s' %(l.label, l.label_source)
            LABEL_LOOKUP[key] = l



    def __unicode__(self):
        return self.researcher

    def save(self):
        if self.prediction_file:
            try:
                self.researcher = self.prediction_file.researcher
                self.prediction_source = self.prediction_file.prediction_source

                parser = LabeledFileParser()
                results = parser.parse(self.prediction_file.get_path())
                
                # Retrieve all records of this researcher
                records = Record.objects.filter(researcher=self.researcher).order_by('record_id')
                
                # Assure that the length are the same
                if len(results) == len(records):
                    for record, result in zip(records, results):
                        print record, result[0], '\n'
                        tokens = Pubtoken.objects.filter(belonging_record=record).order_by('token_sequence_id')
                        for token, label in zip(tokens, result[1]):
                            key = '%s-%s' %(label, self.prediction_source)
                            predicted_label = Validator.LABEL_LOOKUP[key]

                            prev_predicted_label = token.predicted_label.filter(label_source=self.prediction_source)
                            if prev_predicted_label:
                                token.predicted_label.remove(prev_predicted_label[0])
                            token.predicted_label.add(predicted_label)
                            token.save()
                    super(Validator, self).save()
                else:
                    print '[!Validator Model Save] Unequal length!'

            except Exception, e:
                print e
                print 'Save Record Error!!!'

