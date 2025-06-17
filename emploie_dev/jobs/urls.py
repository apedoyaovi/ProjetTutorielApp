from django.urls import path
from jobs import views

urlpatterns = [
    path('offres', views.offres, name='offres'),
    path('créer_un_offre', views.créer_un_offre, name='créer_un_offre'),
    path('détail_offre', views.détail_offre, name='détail_offre'),
]