from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:contact_id>', views.profile, name='profile'),
    path('search/', views.search, name='search'),
]
