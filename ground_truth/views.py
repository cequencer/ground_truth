from django.http import HttpResponse, HttpResponseRedirect, Http404,HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from record.models import Record, Pubtoken, Mode
from label.models import Label
import json

def home(request):
    return HttpResponseRedirect('/align/page/')

def output(request, researcher):
    """
    Output the labeled testing data
    """
    output_txt = ''

    # Get researcher's id
    records = Record.objects.filter(researcher=researcher).order_by('record_id')
    for record in records:
        output_txt += record.record
        tokens = Pubtoken.objects.filter(belonging_record=record).order_by('token_id')
        for token in tokens:
            true_labels = ','.join([true_label.label for true_label in token.true_label.all()])
            output_txt += token.token + '\t' + true_labels + '\n'
        output_txt += '\n'

    return HttpResponse(output_txt, content_type='text/plain')