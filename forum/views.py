import json

from django.contrib.auth import authenticate, login
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

from .models import Section, Thread, Post, User


def index(request):
    section_list = Section.objects.all()
    thread_list = Thread.objects.all()
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = ''

    return render(request, 'index.html', {'sections':section_list, 'threads':thread_list, 'user':current_user})


def safe_call(value, f):
    if value is None:
        return None
    else:
        return f(value)


def threads(request, section_id):
    if request.method == "GET":
        return get_threads(request, section_id)
    else:
        return create_thread(request, section_id)


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


@transaction.atomic()
def create_thread(request, section_id):
    data = json.loads(request.body)
    new_thread = Thread(title=data["title"], section_id=section_id)
    new_thread.save()
    new_post = Post(thread=new_thread, author=request.user, text=data["text"])
    new_post.save()
    new_thread_id = {"id":new_thread.pk}
    return HttpResponse(json.dumps(new_thread_id), content_type="application/json")


def get_posts(request, section_id, thread_id):
    limit = int(request.GET.get('limit', '20'))
    offset = int(request.GET.get('offset', '0'))
    posts = map(model_to_dict, Post.objects.filter(thread=Thread.objects.filter(section=int(section_id)).get(pk=int(thread_id)))[offset:offset + limit])
    return HttpResponse(json.dumps(list(posts)), content_type="application/json")


def login(request):
    return render(request, 'registration/login.html')


def authenticate(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'index.html')
    else:
        return render(request, 'registration/login.html')


def push_thread(request, thread_id):
    db_query = Post.objects.filter(thread=thread_id)
    post_list = db_query.order_by("last_edited_on")
    op = db_query.order_by("last_edited_on").first()
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = ''
    return render(request, "thread_template.html", {'post_list': post_list, 'original_poster': op, 'user': current_user})


def user(request, userid):
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = ''
    selected_user = User.objects.filter(id=userid)
    selected_user_posts = Post.objects.filter(author_id=userid).order_by('created_on')
    username = selected_user[0].username
    first_name = selected_user[0].first_name
    last_name = selected_user[0].last_name
    is_staff = selected_user[0].is_staff
    date_joined = selected_user[0].date_joined
    last_login = selected_user[0].last_login
    post_count = 0
    for i in selected_user_posts:
        post_count += 1
    selected_user_posts = selected_user_posts[:3]
    posts = [{
        "text": post.text,
        "thread": post.thread.title
    } for post in selected_user_posts]
    return render(request, "user.html", {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'is_staff': is_staff,
        'date_joined': date_joined,
        'last_login': last_login,
        'post_count': post_count,
        'posts': posts,
        'user': current_user})

