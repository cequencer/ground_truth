from django.db import models
from ground_truth.settings import MEDIA_ROOT
from pubfile.models import Pubfile
from utils.tokenizer import Tokenizer
from label.models import Label

tokenizer = Tokenizer()

class Mode(models.Model):
    mode = models.BooleanField(default=False)
        

class Record(models.Model):
    record_id = models.AutoField(primary_key=True)
    record = models.TextField(blank=True)
    pubfile = models.ForeignKey(Pubfile, blank=True, null=True)
    researcher = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.record

    def is_labeled(self):
        try:
            tokens = Pubtoken.objects.filter(belonging_record=self)
            for token in tokens:
                if not token.true_label.exists():
                    return False
            return True
        except Exception, e:
            raise e

    def save(self):
        print 'My save called!'
        if self.pubfile:
            try:
                fp = open(self.pubfile.get_path(), 'r')
                for line in fp:
                    new_record = Record(record=line, researcher=self.pubfile.pubfile_name)
                    super(Record, new_record).save()

                    tokens = tokenizer.tokenize(line)['tokens']
                    sequence_id = 0
                    for token in tokens:
                        new_instance = Pubtoken(
                            token=token, 
                            token_sequence_id=sequence_id,
                            belonging_record=new_record)
                        sequence_id += 1
                        try:
                            super(Pubtoken, new_instance).save()
                        except IntegrityError:
                            print 'Save Token Error!!!'   
            except Exception, e:
                print e
                print 'Save Record Error!!!'

class Pubtoken(models.Model):
    token_id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=1000)
    true_label = models.ManyToManyField(Label, blank=True, verbose_name='true label', related_name='true_label')
    predicted_label = models.ManyToManyField(Label, blank=True, verbose_name='predicted label', related_name='predicted_label')
    token_sequence_id = models.IntegerField()
    belonging_record = models.ForeignKey(Record)

    def __unicode__(self):
        return '%s--%s' % (self.belonging_record.record_id, self.token)