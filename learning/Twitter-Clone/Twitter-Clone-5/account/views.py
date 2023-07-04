from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from post.models import Post

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

def account_logout(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

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

def profile(request, username):
	context = {}

	viewingUser = get_object_or_404(User, username=username)
	context["profile"] = viewingUser.profile
	context["isUser"] = False
	if request.user.is_authenticated:
		if request.user.profile == context["profile"]:
			context["isUser"] = True
	
	context["posts"] = Post.objects.filter(author = viewingUser).order_by('-created_on')

	return render(request, 'account/profile.html', context)

