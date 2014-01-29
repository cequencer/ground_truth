from django.http import HttpResponse, HttpResponseRedirect, Http404,HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from validator.models import Validator
from label.models import Label
from record.models import Mode
from django.views.decorators.csrf import csrf_exempt
import json

def stat(request):
    """
    collect all stats about the labeling accuracy, and generate report.
    """
    pass


@csrf_exempt
def change_mode(request):
    if not request.method.lower() == 'post':
        raise Http404
    else:
        cur_mode = request.POST['mode'].split('-')[-1]

        try:
            mode = Mode.objects.all()[0]
            if cur_mode == 'on':
                mode.mode = False
            else:
                mode.mode = True

            mode.save()
            return HttpResponse(json.dumps(True), mimetype='application/json')     
        except Exception, e:
            return HttpResponse(json.dumps(False), mimetype='application/json')     
