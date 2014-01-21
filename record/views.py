from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from record.models import Record, Pubtoken
from label.models import Label
import json
from django.views.decorators.csrf import csrf_exempt

def parse_update_label(label_class, selected_id):
    try:
        selected = int(label_class.split('-')[-1])
        selected_label, token_id = selected_id.split('-')
        token_id = int(token_id)
    except:
        selected = None
        selected_label = None
        token_id = -1

    return selected, selected_label, token_id

def index(request):
    pass


def align(request, record_id):
    record = get_object_or_404(Record, record_id=record_id)
    try:
        tokens = Pubtoken.objects.filter(belonging_record=record).order_by('token_sequence_id')
        available_labels = Label.objects.all().order_by('label_id')

    except Exception, e:
        tokens = []
        print e

    return render_to_response('record/record.html', 
        {'record': record, 'tokens':tokens, 'available_labels':available_labels, })


@csrf_exempt
def update_label(request):
    if not request.method.lower() == 'post':
        return Http404()
    else:
        selected, selected_label_str, token_id = parse_update_label(request.POST['label_class'], request.POST['selected_id'])
        token = get_object_or_404(Pubtoken, token_id=token_id)
        
        if selected:    
            #original true, switch it to false, remove it
            selected_label = get_object_or_404(Label, label=selected_label_str)
            try:
                token.true_label.remove(selected_label)
                token.save()
                return HttpResponse(json.dumps(True), mimetype='application/json')
            except Exception, e:
                print e
                return HttpResponse(json.dumps(False), mimetype='application/json')
        else:           
            #original false, switch it to true, add it
            selected_label = get_object_or_404(Label, label=selected_label_str)
            try:
                token.true_label.add(selected_label)
                token.save()
                return HttpResponse(json.dumps(True), mimetype='application/json')
            except Exception, e:
                print e
                return HttpResponse(json.dumps(False), mimetype='application/json')     

@csrf_exempt
def select_name(request):
    if not request.method.lower() == 'post':
        return Http404()
    else:
        token_id = int(request.POST['selected_id'])
        token = get_object_or_404(Pubtoken, token_id=token_id)
        
        fn_label = get_object_or_404(Label, label='FN')
        ln_label = get_object_or_404(Label, label='LN')
        try:
            token.true_label.add(fn_label)
            token.true_label.add(ln_label)
            token.save()
            return HttpResponse(json.dumps(True), mimetype='application/json')
        except Exception, e:
            print e
            return HttpResponse(json.dumps(False), mimetype='application/json')

@csrf_exempt
def clear_labels(request):
    if not request.method.lower() == 'post':
        return Http404()
    else:
        token_id = int(request.POST['selected_id'])
        token = get_object_or_404(Pubtoken, token_id=token_id)
        
        try:
            token.true_label.clear()
            token.save()
            return HttpResponse(json.dumps(True), mimetype='application/json')
        except Exception, e:
            print e
            return HttpResponse(json.dumps(False), mimetype='application/json')


