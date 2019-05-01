from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from .models import Section, Thread


def index(request):
    section_list = Section.objects.all();
    thread_list = Thread.objects.all();
    return render(request, 'index.html', {'sections':section_list, 'threads':thread_list})


def getThreads(request, section_id):
    limit = int(request.GET.get('limit', '20'))
    offset = int(request.GET.get('offset', '0'))
    threads = Thread.objects.filter(section=int(section_id))[offset:offset+limit]
    return HttpResponse(serializers.serialize('json', threads), content_type="application/json")

