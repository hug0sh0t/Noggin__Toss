from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from django.views.generic import TemplateView
import notifications.urls
# main urls
from accounts.views import (
    login_view,
    logout_view,
    register_view,
    notification_view,
    api_notification_view,
    change_password,
    vault_view,
    codeofconduct_view,
    termsof_service_view,
    remove_account,
    privacy_policy_view,
)

from noggins.views import (
    home_view,
    noggins_list_view,
    noggins_detail_view,
    noggins_delete_view,
    guiCommentSalute,
    guiCommentRemove,
)

from profiles.views import (
    profile_search_view,
    profile_following_view,
    api_rank_view,
)

urlpatterns = [
    path('', home_view),
    re_path(r'apex_admin/', admin.site.urls),
    path('global/', noggins_list_view),
    path('pwchange/', change_password, name='change_password'),
    path('tosser_deactivate/', remove_account),


    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="accounts/forgotpw.html"), 
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/forgotpwsent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/forgotpwform.html"),
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/forgotpwdone.html"),
        name="password_reset_complete"),

    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('query/<str:qselected>/', profile_search_view),
    path('vault/', vault_view),
    path('coc/', codeofconduct_view),
    path('tos/', termsof_service_view),
    path('privacypolicy/', privacy_policy_view),
  
    path('api/rank/<int:userid>/', api_rank_view.as_view()),
    path('following/', profile_following_view),
    path('<int:noggin_id>/', noggins_detail_view),
    path('<int:noggin_id>/blip/', noggins_delete_view),
    path('notifications/', notification_view),
    path('notifications/api/<int:noti_id>', api_notification_view.as_view()),
    path('<int:noggin_id>/blipcmt/<int:comment_id>', guiCommentRemove.as_view()),
    path('api/<int:noggin_id>/<int:comment_id>/like/', guiCommentSalute.as_view()),
    path('api/noggins/', include('noggins.api.urls')),
    re_path(r'profiles?/', include('profiles.urls')),
    re_path(r'api/profiles?/', include('profiles.api.urls'))
]
handler404 = 'accounts.views.error_404_view'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)



