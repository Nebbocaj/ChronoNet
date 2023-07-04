from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def userProfile(request):
    return render(request, 'base/userProfile.html')

@login_required(login_url='login')
def userFriends(request):
    return render(request, 'base/userFriends.html')

@login_required(login_url='login')
def userFeed(request):
    return render(request, 'base/userFeed.html')

def userExplore(request):
    return render(request, 'base/userExplore.html')

def userSearch(request):
    return render(request, 'base/userSearch.html')

