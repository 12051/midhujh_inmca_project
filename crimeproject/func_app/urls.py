from django.urls import path
from . import views

urlpatterns = [
    path('advocate_detail/<int:act>/', views.advocate_detail, name='advocate_detail'),
    path('advocate_public/<int:act>/', views.advocate_public, name='advocate_public'),
]
