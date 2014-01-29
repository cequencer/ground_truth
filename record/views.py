from django.http import HttpResponse, HttpResponseRedirect, Http404,HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from record.models import Record, Pubtoken, Mode
from label.models import Label
import json
from django.views.decorators.csrf import csrf_exempt

def parse_update_label(label_class, selected_id):
    try:
        selected = None
        if 'label-1' in label_class:
            selected = 1
        elif 'label-0' in label_class:
            selected = 0
        # selected = int(label_class.split('-')[-1])
        selected_label, token_id = selected_id.split('-')
        token_id = int(token_id)
    except:
        selected = None
        selected_label = None
        token_id = -1

    return selected, selected_label, token_id


def index(request, pagination='0'):
    pagination = int(pagination)
    RECORDS_PER_PAGE = 100

    try:
        max_id = Record.objects.latest('record_id').record_id
        start_record = pagination * RECORDS_PER_PAGE 
        end_record = pagination * RECORDS_PER_PAGE + 100
        
        if start_record > max_id:
            raise Http404

        if end_record > max_id + 1:
            records = Record.objects.all().order_by('record_id')[start_record:]      
        else:
            records = Record.objects.all().order_by('record_id')[start_record:end_record]

    except Exception, e:
        raise Http404

    return render_to_response('record/index.html',
        {'records':records})


def align(request, record_id):
    record_id = int(record_id)
    record = get_object_or_404(Record, record_id=record_id)

    # find prev and next
    max_id = Record.objects.latest('record_id').record_id
    next = None
    next_id = record_id + 1
    prev = None
    prev_id = record_id - 1
    
    while next is None:
        try:
            if next_id > max_id:
                next = None
                break
            next = Record.objects.get(record_id=next_id)
        except Exception, e:
            next_id += 1
            next = None

    while prev is None:
        try:
            if prev_id < 0:
                prev = None
                break
            prev = Record.objects.get(record_id=prev_id)
        except Exception, e:
            prev_id -= 1
            prev = None        

    try:
        tokens = Pubtoken.objects.filter(belonging_record=record).order_by('token_sequence_id')
        available_labels = Label.objects.filter(label_source=0).order_by('label_id')
    except Exception, e:
        tokens = []
        print e

    mode = Mode.objects.all()[0]

    # pagination managing
    if next is None:
        next_id = record_id
    if prev is None:
        prev_id = record_id

    return render_to_response('record/record.html', 
        {
            'record': record, 
            'tokens':tokens, 
            'available_labels':available_labels, 
            'next_id':next_id,
            'prev_id':prev_id,
            'mode':mode,
        })


@csrf_exempt
def update_label(request):
    if not request.method.lower() == 'post':
        raise Http404
    else:
        selected, selected_label_str, token_id = parse_update_label(request.POST['label_class'], request.POST['selected_id'])
        token = get_object_or_404(Pubtoken, token_id=token_id)
        
        if selected:    
            #original true, switch it to false, remove it
            selected_label = get_object_or_404(Label, label=selected_label_str, label_source=0)
            try:
                token.true_label.remove(selected_label)
                token.save()
                return HttpResponse(json.dumps(True), mimetype='application/json')
            except Exception, e:
                print e
                return HttpResponse(json.dumps(False), mimetype='application/json')
        else:           
            #original false, switch it to true, add it
            selected_label = get_object_or_404(Label, label=selected_label_str, label_source=0)
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
        raise Http404
    else:
        token_id = int(request.POST['selected_id'])
        token = get_object_or_404(Pubtoken, token_id=token_id)
        
        fn_label = get_object_or_404(Label, label='FN', label_source=0)
        ln_label = get_object_or_404(Label, label='LN', label_source=0)
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
        raise Http404
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


