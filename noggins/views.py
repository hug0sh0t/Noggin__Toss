from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404 
from .forms import NogginForm, CommentForm
from .models import Noggin, Comment
from django.contrib.auth.decorators import login_required
from profiles.forms import ProfileFilter
from profiles.models import Profile
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from notifications.signals import notify
from django.db.models import Count

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, "pages/feed.html")

def noggins_list_view(request, *args, **kwargs):
    return render(request, "noggins/list.html")

def noggins_detail_view(request, noggin_id,*args, **kwargs):
    query = Noggin.objects.filter(id=noggin_id)
    post = query.first()
    profilequery = Profile.objects.none()
    if not query.exists():
        messages.error(request, "That Noggin Does Not Exist... ")
        return redirect("/")
    for q in query:
        comment_filter = Noggin.objects.filter(user__username=q.user)
    for c in comment_filter:
        current_noggin_cmt_count = Comment.objects.filter(post=noggin_id)
    if not request.user.is_authenticated:
        messages.error(request, "Only Members May Join Noggin DIGs... ")
        return redirect("/login")
    comments = post.comments.filter(active=True).annotate(comraw=Count('commentlike')).order_by("-comraw")
    new_comment = None
    for c in comments:
        profilecomquery = Profile.objects.filter(user = c.user)
        profilequery  = profilequery | profilecomquery

    if request.method == "GET":
        query.first().eyeball_count.add(request.user)
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.user = request.user
            # Save the comment to the database
            new_comment.save()
            # notify
            stringConvert = str(noggin_id)
            if not request.user == post.user:
                notify.send(request.user, recipient=post.user, verb=' Added A Comment',
                        description=str(noggin_id), public=False, level='warning')
            return redirect("/"+stringConvert)
    else:
        comment_form = CommentForm()
    context = {
        "noggin_id": noggin_id,
        "noggins":query, 
        "magni_nog":post, 
        "comment_count": current_noggin_cmt_count.count(),
        "profiles":profilequery, 
        "comments":comments, 
        "comment_form": comment_form, 
        "new_comment": new_comment,
    }
    return render(request, "noggins/detail.html", context)

def noggins_delete_view(request, noggin_id, *args, **kwargs):
    qs = Noggin.objects.filter(id=noggin_id)
    userquery = qs.filter(user=request.user)
    #doesnt exist
    if not qs.exists():
        messages.info(request,'Sorry, but That is A Restricted Area ')
        return redirect("/")
    #bad user
    if not userquery.exists():
        messages.info(request,'Sorry, but You Cannot Do That')
        return redirect("/")
    convertStr = str(noggin_id)
    obj = userquery.first()
    messages.info(request,' Your Noggin Has Been Deleted')
    obj.delete()
    return redirect("/")


class guiCommentSalute(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, noggin_id=None, comment_id=None, format=None):
        qs = Comment.objects.filter(id=comment_id)
        qs_one = qs.first()
        qs_user = str(qs_one.user)
        liked = False
        if request.user in qs_one.commentlike.all():
            liked = False
            qs_one.commentlike.remove(request.user)
        else:
            liked = True
            qs_one.commentlike.add(request.user)
            if not request.user == qs_one.user:
                notify.send(request.user, recipient=qs_one.user, verb=' Liked Your Comment', description=str(noggin_id), public=False)
        counts = qs_one.commentlike.count()
        data = {"comment_owner": qs_user, "liked":liked, "likescount":counts}
        return Response(data)


class guiCommentRemove(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, noggin_id=None, comment_id=None, format=None):
        qs = Comment.objects.filter(id=comment_id)
        qs_one = qs.first()
        qs_user = str(qs_one.user)
        if request.method == "GET":
            qs_one.delete()
        data = {"comment_owner": qs_user, "Content": qs_one.body}
        return Response(data)

