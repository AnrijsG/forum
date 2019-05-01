import json

from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

from .models import Section, Thread, Post


def index(request):
    section_list = Section.objects.all()
    thread_list = Thread.objects.all()
    return render(request, 'index.html', {'sections':section_list, 'threads':thread_list})


def safe_call(value, f):
    if value is None:
        return None
    else:
        return f(value)


def get_threads(request, section_id):
    limit = int(request.GET.get('limit', '20'))
    offset = int(request.GET.get('offset', '0'))
    db_result = Thread.objects.filter(section=int(section_id))[offset:offset+limit]
    threads = [{
        "id": thread.id,
        "title": thread.title,
        "first_post": safe_call(Post.objects.filter(thread=thread.id).order_by("last_edited_on").first(), model_to_dict),
        "author": Post.objects.filter(thread=thread.id).order_by("last_edited_on").first().author.username
    } for thread in db_result]
    return HttpResponse(json.dumps(threads), content_type="application/json")


def get_posts(request, section_id, thread_id):
    limit = int(request.GET.get('limit', '20'))
    offset = int(request.GET.get('offset', '0'))
    posts = map(model_to_dict, Post.objects.filter(thread=Thread.objects.filter(section=int(section_id)).get(pk=int(thread_id)))[offset:offset + limit])
    return HttpResponse(json.dumps(list(posts)), content_type="application/json")

