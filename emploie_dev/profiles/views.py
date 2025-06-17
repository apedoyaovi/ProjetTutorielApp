from django.shortcuts import render

# Create your views here.

def détail_profile(request):
    return render(request, 'profiles/détail_profile.html')

def profiles(request):
    return render(request, 'profiles/profiles.html')

def créer_profile(request):
    return render(request, 'profiles/créer_profile.html')