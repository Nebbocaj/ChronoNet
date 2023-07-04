from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from post.models import Post
from .models import Profile

#Register an account with our system
def account_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request=request, template_name='account/register.html', context={'register_form': form})

#Login to an existing account
def account_login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="account/login.html", context={"login_form":form})

#Logout of an account that is currently logged in
def account_logout(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

#The page where a user can update their profile
@login_required
def profileUpdate(request):
    if request.method == 'POST':
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, f'Account has been updated.')
            return redirect('update_profile')
    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'account/update_profile.html', {'userForm': userForm, 'profileForm': profileForm})

#This is the main profile page
def profile(request, username):
	context = {}

	viewingUser = get_object_or_404(User, username=username)
	context["profile"] = viewingUser.profile
	context["isUser"] = False
	if request.user.is_authenticated:
		if request.user.profile == context["profile"]:
			context["isUser"] = True
	
	posts = Post.objects.filter(author = viewingUser).order_by('-created_on')
	if request.user.is_authenticated:
		posts = Post.objects.annotateWithVote(posts, request.user)
	posts = Post.objects.paginate(posts, request.GET.get('page'))
	context["page_obj"] = posts


	return render(request, 'account/profile.html', context)

#Follow (or unfollow if already following) a profile
@login_required
def follow(request):
	if request.method =="POST" and request.is_ajax():
		# get values
		myProfile = request.user.profile
		profile_id = int(request.POST.get("profile_id",None))
		viewingProfile = get_object_or_404(Profile,pk=profile_id)
		following = myProfile.follow(viewingProfile)

		return JsonResponse({
            "following":following
            })

#Delete profile that is logged in
@login_required
def delete(request):
	if request.method =="POST" and request.is_ajax():
		request.user.delete()

		return JsonResponse({
            "deleted":True
            })