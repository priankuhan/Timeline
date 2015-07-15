from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render
from couchdbkit.ext.django.schema import *
from couchdbkit.ext.django.forms import *
from timeline import models as m
from couchdbkit import *
from datetime import datetime
from operator import itemgetter
import time

class ItemForm(DocumentForm):    
     class Meta:
         document = m.Item

SERVER = Server('http://127.0.0.1:5984/')

def index(request,type=""):
    titles = []
    items = SERVER['item']
    for doc in items:
        item = items[doc["id"]]
        if type == "": 
            titles.append(item)            
        else:
            if item['type'].lower() == type.lower():
                titles.append(item)

            
    titles = sorted(titles, key=itemgetter('time'), reverse=True)
    if request.method == "POST":
        title = request.POST['title']
        dat = datetime.today
        item = {'title': title,'text': "", 'type': "", 'time':int(time.time()), 'date': datetime.now().strftime('%B %-d, %Y - %-I:%M%P') }
        items.save_doc(item)
        docid = item['_id']
        item['url'] = docid
        items[docid] = item
        return HttpResponseRedirect(u"/doc/%s/" % docid)
    return render(request,'index.html',{'rows': titles,'type':type})
    
def detail(request,id):
    items = SERVER['item']
    try:
        item = items[id]
    except ResourceNotFound:
        raise Http404a
    if request.method =="POST":
        item['title'] = request.POST['title']
        item['text'] = request.POST['text']
        item['type'] = request.POST['type']
        items[id] = item
    return render(request,'detail.html',{'row':item})