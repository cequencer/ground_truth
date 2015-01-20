from django.http import HttpResponse, HttpResponseRedirect, Http404,HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from validator.models import Validator
from label.models import Label
from record.models import Record, Pubtoken, Mode
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    try:
        researchers = set(r.researcher for r in Record.objects.all())
    except:
        researchers = []
    return render_to_response('validator/index.html', {'researchers':researchers})


def stat(request, researcher):
    """
    Collect all stats about the labeling accuracy, and generate report.
    Measurement:
    Precision overall
    Precision on every label
    Recall overall
    Recall on every label
    """
    try:
        records = Record.objects.filter(researcher=researcher)
        tokens = Pubtoken.objects.filter(belonging_record__in=records)

        stanfordner_tokenwise_total_hit = 0
        stanfordner_tokenwise_total_miss = 0
        crfsuite_tokenwise_total_hit = 0
        crfsuite_tokenwise_total_miss = 0

        # stanfordner_fn_tp = 0
        # stanfordner_fn_tn = 0
        # stanfordner_fn_fp = 0
        # stanfordner_fn_fn = 0

        # stanfordner_ln_tp = 0
        # stanfordner_ln_tn = 0
        # stanfordner_ln_fp = 0
        # stanfordner_ln_fn = 0

        # stanfordner_dl_tp = 0
        # stanfordner_dl_tn = 0
        # stanfordner_dl_fp = 0
        # stanfordner_dl_fn = 0

        # stanfordner_ti_tp = 0
        # stanfordner_ti_tn = 0
        # stanfordner_ti_fp = 0
        # stanfordner_ti_fn = 0

        # stanfordner_vn_tp = 0
        # stanfordner_vn_tn = 0
        # stanfordner_vn_fp = 0
        # stanfordner_vn_fn = 0

        # stanfordner_yr_tp = 0
        # stanfordner_yr_tn = 0
        # stanfordner_yr_fp = 0
        # stanfordner_yr_fn = 0

        # crfsuite_fn_tp = 0
        # crfsuite_fn_tn = 0
        # crfsuite_fn_fp = 0
        # crfsuite_fn_fn = 0

        # crfsuite_ln_tp = 0
        # crfsuite_ln_tn = 0
        # crfsuite_ln_fp = 0
        # crfsuite_ln_fn = 0

        # crfsuite_dl_tp = 0
        # crfsuite_dl_tn = 0
        # crfsuite_dl_fp = 0
        # crfsuite_dl_fn = 0

        # crfsuite_ti_tp = 0
        # crfsuite_ti_tn = 0
        # crfsuite_ti_fp = 0
        # crfsuite_ti_fn = 0

        # crfsuite_vn_tp = 0
        # crfsuite_vn_tn = 0
        # crfsuite_vn_fp = 0
        # crfsuite_vn_fn = 0

        # crfsuite_yr_tp = 0
        # crfsuite_yr_tn = 0
        # crfsuite_yr_fp = 0
        # crfsuite_yr_fn = 0
     

        for token in tokens:
            true_labels = token.true_label.all()
            stanfordner_label = token.predicted_label.filter(label_source=1)[0]
            crfsuite_label = token.predicted_label.filter(label_source=2)[0]
            if stanfordner_label in true_labels:
                stanfordner_tokenwise_total_hit += 1
                # if stanfordner_label.label == 'FN':
                #     stanfordner_fn_tp += 1
            else:
                stanfordner_tokenwise_total_miss += 1

            if crfsuite_label in true_labels:
                crfsuite_tokenwise_total_hit += 1
            else:
                crfsuite_tokenwise_total_miss += 1

        print '%s:\nstanfordner: %s\ncrfsuite: %s' % (researcher, float(stanfordner_tokenwise_total_hit)/(stanfordner_tokenwise_total_hit+stanfordner_tokenwise_total_miss), float(crfsuite_tokenwise_total_hit)/(crfsuite_tokenwise_total_hit+crfsuite_tokenwise_total_miss))
        return HttpResponse('%s:\nstanfordner: %s\ncrfsuite: %s' % (researcher, float(stanfordner_tokenwise_total_hit)/(stanfordner_tokenwise_total_hit+stanfordner_tokenwise_total_miss), float(crfsuite_tokenwise_total_hit)/(crfsuite_tokenwise_total_hit+crfsuite_tokenwise_total_miss)))

    except Exception, e:
        raise e



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
