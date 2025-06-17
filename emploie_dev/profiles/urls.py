from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles', views.profiles, name='profiles'),
    path('détail_profile', views.détail_profile, name='détail_profile'),
    path('créer_profile', views.créer_profile, name='créer_profile'),
]