from django.shortcuts import render

# Create your views here.

def détail_offre(request):
    return render(request, 'jobs/détail_offre.html')

def offres(request):
    return render(request, 'jobs/offres.html')

def créer_un_offre(request):
    return render(request, 'jobs/créer_un_offre.html')