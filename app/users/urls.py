from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    path('auth/password/', auth_views.PasswordChangeView.as_view(
        template_name='users/change_password.html'),
         name='password_change'),
    path('auth/password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/change_password_done.html'),
         name='password_change_done'),
]
