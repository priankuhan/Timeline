from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render
from couchdbkit.ext.django.schema import *
from couchdbkit.ext.django.forms import *
from timeline import models as m
from couchdbkit import *
from datetime import datetime
from operator import itemgetter
import time
import json

from timeline.models import Uploader

class ItemForm(DocumentForm):    
     class Meta:
         document = m.Item

SERVER = Server('https://couchdb-04a019.smileupps.com')

def index(request,type=""):
    titles = []
    htmldata = []
    items = SERVER['item']
    for doc in items:
        item = items[doc["id"]]
        if item.get('title','') == "":
          items.delete_doc(item)
        if type == "" : 
            titles.append(item)            
        else:
            if item['type'].lower() == type.lower() and item.get('title','') != "":
                titles.append(item)
    titles = sorted(titles, key=itemgetter('time'), reverse=True)
    
    for item in titles:
        if item['type'].lower() == "video":
            item['html'] = "<video width=&quot;500&quot; height=&quot;400&quot; controls><source src=&quot;/static/media/"+item['text']+"&quot; type=&quot;video/mp4&quot;>Your browser does not support the video element.</video>"
        elif item['type'].lower() == "music":
            item['html'] = "<audio controls><source src=&quot;/static/media/"+item['text']+"&quot; type=&quot;audio/mpeg&quot;>Your browser does not support the audio element.</audio>"
        elif item['type'].lower() == "picture":
            item['html'] = "<img class=&quot;img-responsive&quot; src=&quot;/static/media/"+item['text']+"&quot;>"
        elif item['type'].lower() == "other":
            stri = "<p>"+item["text"]+"</p>"
            stri = stri.replace("'", "&quot;")
            stri = stri.replace('"', "&quot;")
            item['html'] = stri
        else:
            item['html'] = "<embed src=&quot;/static/media/"+item['text']+"&quot; width=&quot;500&quot; style=&quot;height:50vh&quot; alt=&quot;pdf&quot; pluginspage=&quot;http://www.adobe.com/products/acrobat/readstep2.html&quot;>"
        items.save_doc(item)
        
            
    if request.method == "POST":
        title = request.POST['title']
        dat = datetime.today
        item = {'title': title.replace("'", ''),'text': "", 'type': "Document", 'time':int(time.time()), 'date': datetime.now().strftime('%B %-d, %Y - %-I:%M%P') }
        items.save_doc(item)
        docid = item['_id']
        item['url'] = docid
        items[docid] = item
        return HttpResponseRedirect(u"/doc/%s/" % docid)
    return render(request,'index.html',{'rows': titles,'type':type,'jsonrows': json.dumps(titles)})

def detail(request,id):
    items = SERVER['item']
    try:
        item = items[id]
    except ResourceNotFound:
        raise Http404a
    if request.method =="POST":
        newdoc = Uploader(docfile = request.FILES['docfile'])
        
        item['title'] = request.POST['title'].replace("'", '')
        item['text'] = request.FILES['docfile'].name.replace("'", '').replace(" ","_")
        item['type'] = request.POST['type'].replace("'", '')
        item['time'] = int(time.time())
        item['date'] = datetime.now().strftime('%B %-d, %Y - %-I:%M%P')
        
        if item['type'].lower() == "video":
            item['html'] = "<iframe width='420' height='315'src='"+item['text']+"'></iframe>"
        elif item['type'].lower() == "music":
            item['html'] = "<audio controls><source src='"+item['text']+"' type='audio/mpeg'>Your browser does not support the audio element.</audio>"
        elif item['type'].lower() == "picture":
            item['html'] = "<img src='{% static 'media/"+item['text']+"' %}'>"
        elif item['type'].lower() == "other":
            stri = "<p>"+item["text"]+"</p>"
            stri = stri.replace("'", "&quot;")
            stri = stri.replace('"', "&quot;")
            item['html'] = stri
        else:
            stri = "<p>"+item["text"]+"</p>"
            stri = stri.replace("'", "&quot;")
            stri = stri.replace('"', "&quot;")
            item['html'] = stri
        items[id] = item
        
        try:
          newdoc.save()
        except: 
          pass
        return HttpResponseRedirect(u"/")
    return render(request,'detail.html',{'row':item})