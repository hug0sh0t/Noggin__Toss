from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.signals import post_save
from notifications.signals import notify
from django.db.models import Count

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from ..forms import NogginForm
from ..models import Noggin
from ..serializers import (
    NogginSerializer,
    NogginActionSerializer,
    NogginCreateSerializer
)
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

#DJANGO REST api integrations 
@api_view(['POST','GET']) 
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def noggin_create_view(request, *args, **kwargs):
    parser_classes = (MultiPartParser, FormParser)
    # changing data  from request.POST, to request.data 
    serializer = NogginCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def noggin_detail_view(request, noggin_id, *args, **kwargs):
    qs = Noggin.objects.filter(id=noggin_id)
    if not qs.exists():
        return Response({"message":"ERROR"}, status=404)
    obj = qs.first()
    serializer = NogginSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def noggin_delete_view(request, noggin_id, *args, **kwargs):
    #if nogginID doesnt exist, 404
    qs = Noggin.objects.filter(id=noggin_id)
    if not qs.exists():
        return Response({}, status=404)
    #if improper user, unauthorized
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "unauthorized noggin Removal 403"}, status=403)
    obj = qs.first()
    obj.delete()
    #otherwise success
    return Response({"message": "Noggin Removed"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def noggin_action_view(request, *args, **kwargs):
    serializer = NogginActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        noggin_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        image = data.get("image")
        qs = Noggin.objects.filter(id=noggin_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = NogginSerializer(obj)
            # notify.send(recipient, actor, verb, description, level, public, level="information")
            if not request.user == obj.user:
                notify.send(request.user, recipient=obj.user, verb=' Saluted Your Noggin!', 
                        description=str(noggin_id), public=False, level='success')
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = NogginSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "relay":
            new_noggin = Noggin.objects.create(
                    user=request.user,
                    parent=obj,
                    content=content,
                    image=image,
                    )
            serializer = NogginSerializer(new_noggin)
            return Response(serializer.data, status=201)
    return Response({}, status=200)

#HOW MANY NOGGINS PER PAGE ~
def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = NogginSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def noggin_feed_view(request, *args, **kwargs):
    user = request.user
    qs = Noggin.objects.feed(user)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def noggin_list_view(request, *args, **kwargs):
    qs = Noggin.objects.all().annotate(numraw=Count('likes')).order_by('-numraw')
    username = request.GET.get('username')
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)

# django RESTAPI frame above 
# LIC. under Creator Seanchester Reyes Rosario

