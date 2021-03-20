from django.urls import path

from .views import (
    noggin_action_view,
    noggin_delete_view,
    noggin_detail_view,
    noggin_feed_view,
    noggin_list_view,
    noggin_create_view,
)
'''
CLIENT ~> /api/noggins/
'''

urlpatterns = [
    path('', noggin_list_view),
    path('feed/', noggin_feed_view),
    path('action/', noggin_action_view),
    path('create/', noggin_create_view),
    path('<int:noggin_id>/', noggin_detail_view),
    path('<int:noggin_id>/delete/', noggin_delete_view),
]


