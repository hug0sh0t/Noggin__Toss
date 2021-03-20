from django.http import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import ProfileForm, ProfileFilter, NogginFilter, UserFilter
from .models import Profile
from noggins.models import Noggin, Comment
from django.contrib.auth import get_user_model
from itertools import chain
from django.contrib import messages
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.db.models import F
from django.db.models import Q

User = get_user_model()

def profile_base_view(request, *args, **kwargs):
    user = request.user
    path = "/profiles/"
    return redirect(path+user.username)

def profile_update_view(request, *args, **kwargs):
    profileQuery = Profile.objects.all()
    # pquery_obj = profileQuery.first()
    userQ = profileQuery.filter(user=request.user)

    if not request.user.is_authenticated:
        return redirect("/login?next=/profile/update")
    user = request.user
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }
    my_profile = user.profile
    post_data = request.POST or None 
    file_data = request.FILES or None
    form = ProfileForm(post_data, file_data, instance=my_profile, initial=user_data)
    if form.is_valid():
        profile_obj = form.save(commit=False)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        # solution
        avatar = form.cleaned_data.get('avatar')
        user.first_name = first_name
        user.last_name = last_name
        #solution
        user.avatar = avatar
        user.email = email
        user.save()
        profile_obj.save()
        return HttpResponseRedirect(user.username)
    context = {
        "form": form,
        "users": userQ,
        "profiles":profileQuery,

    }
    return render(request, "profiles/remodel.html", context)

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


class api_rank_view(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, userid=None, format=None):
        query = Profile.objects.filter(user = userid)
        comment_query = Comment.objects.filter(user_id = userid)
        self_decoy_filter = Profile.objects.none()
        self_com_decoy_filter = Profile.objects.none()
        container = 0
        ibadge_container = 0
        hbadge_container = 0
        thunder = 0
    
        for c in comment_query:
            self_com_decoy_filter = self_com_decoy_filter | c.commentlike.filter(id = userid)
            container += c.commentlike.count()
        #Special Equation For Comments / filter self likes
        hbadge_container = container - self_com_decoy_filter.count() 

        firstquery = query.first()
        current_username = firstquery.user
        # cValue = firstquery.createBadge
        nogginQs = Noggin.objects.filter(user_id=userid)
        firstnoggin_qs = nogginQs.first()
        amountsal = 0
        for n in nogginQs:
            self_decoy_filter = self_decoy_filter | n.likes.filter(id = userid)
            amountsal += n.likes.count()

        #Special Equation For Noggins / filter self salutes
        ibadge_container = amountsal - self_decoy_filter.count() 

        thunder += firstquery.createBadge
        thunder += firstquery.impactBadge
        thunder += firstquery.hermesBadge
    
        Profile.objects.filter(user_id = userid).update(impactBadge = ibadge_container*2)
        Profile.objects.filter(user_id = userid).update(hermesBadge = hbadge_container*1.75)
        Profile.objects.filter(user_id = userid).update(createBadge = nogginQs.count()*1.5)
        Profile.objects.filter(user_id = userid).update(FavoredBadge = thunder/3)
         
        data = {"rankOwner": str(current_username),"amount of Noggins": nogginQs.count(), 
                "cBadge": firstquery.createBadge,
                "impactBadge": firstquery.impactBadge,"hBadge": firstquery.hermesBadge,
                "ThunderBadge": firstquery.FavoredBadge}
        return Response(data)

def profile_detail_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    nogginQs = Noggin.objects.filter(user__username=username)
    commentQs = Comment.objects.filter(user__username=username)
        
    amountSal = 0
    amountCmtSal = 0
    is_following = False
    profile_obj = qs.first()

    impactRatio140 = (profile_obj.impactBadge / 150)* 100
    hermesRatio140 = (profile_obj.hermesBadge / 140)* 100
    createRatio140 = (profile_obj.createBadge / 140)* 100
    thunderRatio140 = (profile_obj.FavoredBadge / 150)* 100

    nogginqs_obj = nogginQs.first()
    if not qs.exists():
        messages.info(request, "That Member Doesnt Exist ... ")
        return redirect ("/")
    if request.user.is_authenticated:
        user = request.user
        is_following = user in profile_obj.followers.all()
    else:
        messages.info(request, "Only Members May View Profiles ... ")
        return redirect("/login")
    for c in commentQs:
        amountCmtSal += c.commentlike.count()
    for n in nogginQs:
        amountSal += n.likes.count()
    context = {
        "username": username,
        "c_ratio": int(createRatio140), 
        "i_ratio": int(impactRatio140), 
        "h_ratio": int(hermesRatio140), 
        "t_ratio": int(thunderRatio140), 
        "profile": profile_obj,
        "salute_amount": human_format(amountSal),
        "cmt_interact_salute": human_format(amountCmtSal),
        "is_following": is_following,
    }
    return render(request, "profiles/detail.html", context)

def profile_followers_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    fullqs = Profile.objects.none()
    user_qs = qs.first()
    followers_list = user_qs.followers.all()
    first_qs = followers_list.first()
    for f in followers_list:
        id_follower_qs = Profile.objects.filter(user=f.id)
        fullqs = fullqs | id_follower_qs
    context = {
        "gui": fullqs,
    }
    return render(request, "profiles/followers.html", context)

def profile_following_view(request):
    filter = ProfileFilter(request.GET, queryset=Profile.objects.all())
    context = {
        "filter": filter,
    } 
    return render(request, 'profiles/following.html', context)


def profile_search_view(request, qselected):
    f = ProfileFilter(request.GET,queryset=Profile.objects.filter(
        Q(user__username__contains=str(qselected))|
        Q(user__first_name__icontains=str(qselected))|
        Q(user__last_name__icontains=str(qselected))))
    n = NogginFilter(request.GET,queryset=Noggin.objects.filter(Q(content__contains=str(qselected))))
    allprofiles = Profile.objects.all()
    userqs = User.objects.all()
    search_q = request.GET.get('valuebox', None)
    if search_q:
        return redirect("/query/"+search_q+"/")
    context = {
            "userqs": userqs,
            "profiles": allprofiles,
            "query": qselected,
            "filter": f,
            "nogfilter": n,
    } 
    return render(request, 'profiles/search.html', context)

 

