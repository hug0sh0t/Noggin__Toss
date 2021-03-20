from django.urls import path

from .views import profile_base_view, profile_detail_view, profile_update_view, profile_followers_view

urlpatterns = [
    path('edit', profile_update_view),
    path('<str:username>/followers', profile_followers_view),
    path('vault', profile_base_view),
    path('<str:username>', profile_detail_view),

]
