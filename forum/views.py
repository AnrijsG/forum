import json

from django.contrib.auth import authenticate, login, forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import UserForm
from .models import Section, Thread, Post, User, UserGroup


def index(request):
    section_list = Section.objects.all()
    thread_list = Thread.objects.all()
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = ''

    return render(request, 'Index/index.html', {'sections':section_list, 'threads':thread_list, 'user':current_user})


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


@login_required
@permission_required(perm='add_thread', raise_exception=True)
@transaction.atomic
def create_thread(request, section_id):
    data = json.loads(request.body)
    new_thread = Thread(title=data["title"], section_id=section_id)
    new_thread.save()
    new_post = Post(thread=new_thread, author=request.user, text=data["text"])
    new_post.save()
    new_thread_id = {"id":new_thread.pk}
    return HttpResponse(json.dumps(new_thread_id), content_type="application/json")


def show_thread(request, thread_id):
    page = int(request.GET.get('page', '1'))
    all_posts = Post.objects.order_by('created_on').filter(thread=thread_id)
    first_post = all_posts[0]

    paginator = Paginator(all_posts.exclude(id=first_post.pk), 5)

    posts = paginator.get_page(page)
    db_query = Post.objects.filter(thread=thread_id)
    op = db_query.order_by("last_edited_on").first()

    return render(request, "ThreadTemplate/thread_template.html", {'first_post': first_post, 'post_list': posts, 'original_poster': op})


def authenticate(request):
    user = authenticate(request, username=forms.username, password=forms.password)
    if user is not None:
        login(request, user)
        return render(request, 'Index/index.html')
    else:
        return render(request, 'registration/login.html')


def user(request, userid):
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = ''
    selected_user = User.objects.filter(id=userid)
    selected_user_posts = Post.objects.filter(author_id=userid).order_by('-created_on')
    username = selected_user[0].username
    first_name = selected_user[0].first_name
    last_name = selected_user[0].last_name
    is_staff = selected_user[0].is_staff
    is_su = selected_user[0].is_superuser
    date_joined = selected_user[0].date_joined
    last_login = selected_user[0].last_login
    is_active = selected_user[0].is_active
    post_count = 0
    for i in selected_user_posts:
        post_count += 1
    selected_user_posts = selected_user_posts[:3]
    posts = [{
        "text": post.text,
        "thread": post.thread.title,
        "created_on": post.created_on
    } for post in selected_user_posts]
    return render(request, "User/user.html", {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'is_staff': is_staff,
        'is_su': is_su,
        'is_active': is_active,
        'date_joined': date_joined,
        'last_login': last_login,
        'post_count': post_count,
        'posts': posts,
        'user': current_user})


@login_required
@permission_required(perm='add_post', raise_exception=True)
def post_reply(request, thread_id):
    data = json.loads(request.body)
    new_post = Post(thread_id=thread_id, author=request.user, text=data["text"])
    #new_post = Post.objects.create(thread_id=thread_id, author=request.user, text=data["text"])
    new_post.save()
    return HttpResponse()


@login_required
@permission_required(perm='change_post', raise_exception=True)
def post_edit(request, post_id):
    text = Post.objects.filter(id=post_id)[0]
    if request.user.pk == text.author_id or request.user.is_staff:
        return render(request, 'edit/edit_template.html', {'text': text})
    else:
        return index(request)


@login_required
@permission_required(perm='change_post', raise_exception=True)
def post_edit_go(request, post_id):
    text = request.POST.get('text')
    post = Post.objects.get(id=post_id)
    if post.text != text:
        post.text = text
        post.save()

    return redirect('/threads/' + str(post.thread.pk))


@login_required
@permission_required(perm='delete_user', raise_exception=True)
def deactivate(request):
    if request.user.is_staff:
        username = json.loads(request.body)
        user = User.objects.get(username=username['username'])
        if not user.is_superuser:
            if user.is_active:
                user.is_active = False
                user.save()
            else:
                user.is_active = True
                user.save()
    return HttpResponse()


@login_required
@permission_required(perm='delete_post', raise_exception=True)
def post_delete(request, delete_id):
    post = Post.objects.get(id=delete_id)
    if request.user == post.author or request.user.is_staff:
        post.delete()
    return HttpResponse()


def register(request):
    user_form = UserForm(data=request.POST)
    if request.method == "POST":
        if not request.user.is_authenticated:
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                usergroup = UserGroup.objects.get(id='2')
                usergroup.save()
                user.save()
                return index(request)
            else:
                return render(request, 'registration/register.html', {'user_form': user_form, 'errors': user_form.errors})
        else:
            return HttpResponse('You are already logged in!')
        return render(request, 'registration/register.html', {'user_form': user_form, 'errors': ''})
    else:
        return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
@permission_required(perm='delete_thread', raise_exception=True)
def delete_thread(request):
    if request.user.is_staff:
        thread_id = json.loads(request.body)
        thread = Thread.objects.get(id=thread_id['threadId'])
        thread.delete()
    return HttpResponse()
