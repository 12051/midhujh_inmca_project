from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('victimregister/', views.victimregister, name='victimregister'),
    path('witnessregister/', views.witnessregister, name='witnessregister'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('user/<int:user_id>', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)