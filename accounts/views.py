from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.db.models.signals import post_save
from notifications.signals import notify
from noggins.models import Noggin,Comment
from profiles.models import Profile
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
User = get_user_model()

def error_404_view(request, exception):
    return render(request, "404.html")

# Noggin User authentication process
def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        if str(request.user.email).strip() == ' ' or str(request.user.email).strip() == '':
            messages.info(request,'Please Enter Your Email')
            return redirect("/profiles/edit")
        elif '@' not in str(request.user.email).strip():
            messages.info(request,'Please Enter a Valid Email')
            return redirect("/profiles/edit")
        greeting = 'Welcome '+str(request.user)
        messages.info(request, greeting)
        return redirect("/")
    context = {
        "form": form,
        "btn_label": "Enter",
    }
    
    return render(request, "accounts/enter.html", context)


def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        messages.info(request,'BYE, COME AGAIN！')
        logout(request)
        return redirect("/login")
    context = {
        "form": None,
        "btn_label": "CONFIRM",
        "title": "leaving? "
    }
    return render(request, "accounts/auth.html", context)

# 12/10/2020, register was changed
def register_view(request , *args, **kwargs):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Your Account was Successfuly Created, Please Loggin')
            return redirect('/login')

    else:
        f = CustomUserCreationForm()
    context = {
        "form": f,
        "description": "Your Username is Permanent, So Please Choose Wisely",
        "btn_label": "JOIN",
    }

    return render(request, 'accounts/register.html', context)

def codeofconduct_view(request, *args, **kwargs):
    context = {
        "title":"ＣＯＤＥ ＯＦ ＣＯＮＤＵＣＴ",
    }
    return render(request, "accounts/cOc.html", context)

def termsof_service_view(request, *args, **kwargs):
    context = {
        "title":"ＴＨＥ ＬＥＧＡＬＩＴＩＥＳ",
    }

    return render(request, "accounts/tos.html", context)

def privacy_policy_view(request, *args, **kwargs):
    context = {
        "title":"ＤＡＴＡ , ＡＮＤ ＷＨＡＴ ＷＥ ＤＯ ＷＩＴＨ ＩＴ",
    }

    return render(request, "accounts/privacy.html", context)


def vault_view(request, *args, **kwargs):
    user = User.objects.get(username=request.user)
    profileNotBin = Profile.objects.none()
    allprofile = Profile.objects.all()
    fullnogqs = Noggin.objects.all()
    decoybin = Noggin.objects.none()
    insertion = Noggin.objects.none()
    finalinsert = Noggin.objects.none()
    commentinsert = Comment.objects.none()

    commentbin = Comment.objects.all()
    commentfinal = Comment.objects.all()
    commentunite = Comment.objects.none()
    for s in fullnogqs:
        test = s.likes.filter(username=request.user)
        decoybin = s.likes.values_list("noggin_user", flat=True).filter(username=request.user)
        if decoybin:
            insertion = insertion |  decoybin
    for i in insertion:
        finalquery = Noggin.objects.filter(id=i)
        finalinsert = finalinsert | finalquery
    for c in commentbin:
        commentbin = c.commentlike.values_list("commenter", flat=True).filter(username = request.user)
        commentinsert = commentinsert | commentbin
        # print(c.commentlike.filter(username = request.user))
    for final in commentinsert:
        commentfinal = Comment.objects.filter(id=final)
        commentunite = commentunite | commentfinal
    context = {
            "salutednoggins": finalinsert,
            "profiles": allprofile,
            "salutedcomments": commentunite,
    }
    return render(request, "accounts/vault.html", context)

def notification_view(request, *args, **kwargs):
    user = User.objects.get(username=request.user)
    profileNotBin = Profile.objects.none()
    allprofile = Profile.objects.all()
    goneqs = user.notifications.deleted()
    blindqs = user.notifications.unread()
    seeqs = user.notifications.read()
    allqs = user.notifications.all()
    alllistqs = list(allqs)
    for a in alllistqs:
        if str(a.actor).strip() == "None":
            a.delete()
        profileNotQuery = Profile.objects.filter(user = a.actor)
        profileNotBin = profileNotBin | profileNotQuery 
  
    if request.method == "GET":
        blindqs.mark_all_as_read(request.user)
    # marked as deleted, are deleted
    goneqs.delete()
    context = {
        "allnots": alllistqs,
        "profiles": allprofile, 
        "profilenots": list(profileNotBin),
    }
    
    return render(request, "accounts/notifications.html", context)


class api_notification_view(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, noti_id=None, format=None):
        user = User.objects.get(username=request.user)
        profileNotBin = Profile.objects.none()
        seeqs = user.notifications.read()
        allqs = user.notifications.all()
        for s in seeqs:
            notificationfilter = user.notifications.filter(id=noti_id)
        print(notificationfilter)
        if request.method == "GET":
            print(noti_id)
            notificationfilter.delete()
        data = {"OWNER OF NOTIFICATIONS: ": user.username, "notification ID": noti_id}
        return Response(data)


def change_password(request):
    if request.user.is_authenticated: 
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.info(request, 'Your password was successfully updated! Please Try it Out ')
                logout(request)
                return redirect("/login")
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {'form': form})

    else:
        messages.info(request, "Only Authorized Members Can be There ... ")
        return redirect('/login')
 

@require_http_methods(['GET'])
def remove_account(request):
    user_pk = request.user.pk
    auth_logout(request)
    User = get_user_model()
    User.objects.filter(pk=user_pk).delete()

    messages.info(request, "Your Account has been Successfully Deactivated ...  ")
    return redirect('/login')


