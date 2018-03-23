from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.shortcuts import redirect


def redirect_users_team_page(view_func):
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/team')
        return view_func(request, *args, **kwargs)
    return _wrapped


urlpatterns = [
    path('team/', views.generic_team, name='generic_team'),
    path('team/<slug:symbol>', views.team, name='team'),

    path('pusher_auth', views.pusher_auth, name='pusher_auth'),

    # Auth views
    path('logout/', auth_views.logout, name='logout'),
    path('', redirect_users_team_page(
        auth_views.LoginView.as_view(template_name='index.html')
    ), name='index'),

]
