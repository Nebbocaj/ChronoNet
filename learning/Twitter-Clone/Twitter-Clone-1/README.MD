
# Setup

Use Python 3.7.11. The dependencies can be installed using `pip install -r requirements.txt`.

Create Django project, (I rename the projects subfolder `config`).
``` shell
mkdir Twitter-Clone-1
cd Twitter-Clone-1
django-admin startproject config .
```

Create an app `account`, add it to the settings and import to urls `account/`. Add a `urls.py` to `accounts`.
``` python
    path('account/', include('account.urls'))
```

Also add `crispy_forms` to your settings imported apps, we will use it later. Add to the end of your settings `CRISPY_TEMPLATE_PACK = 'bootstrap4'`.

Create and add to settings the `templates` folder. Add the `templates/account` folder to `account`. Create a base, navbar, and home page in the base templates folder 

###### templates/navbar.html 
``` html
<nav class="navbar navbar-expand-md navbar-light bg-light">
    <div class="container">
        <div class="collapse navbar-collapse" id="navbarToggle">
            <div class="navbar-nav pr-2">
                This is a navbar
            </div>
        </div>
    </div>
</nav>
```
###### templates/base.html 
``` html
{% load static %}
<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
        integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
     <title>Twitter clone 1</title>
</head>

<body>
    <header class="site-header">
        {% include 'navbar.html' %}
    </header>
    <main role="main" class="container-fluid">
        <br>
        <div class="row">
            <div class="col-md-12">
                {% if messages %}
                {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
                {% endfor %}
                {% endif %}
                {% block content %}{% endblock %}
            </div>
        </div>
    </main>
</body>

</html>
```

###### templates/home.html 
``` html
<div class="container">
This is a home page.
{% if user.is_authenticated %}
  Hi {{ user.username }}!
{% else %}
  <p>Please log in</p>
{% endif %}
</div>
```

Create a base url that directs to the homepage (no need for anything fancy right now).
``` python
    path('', TemplateView.as_view(template_name='home.html'), name='home'),    
```

Migrate, run, and check everything is working

## Account
 Lets do this all at once. Start with adding the urls we will need (well add the views in a moment)

###### account/urls.py
``` python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.account_register, name="register"),
    path('login/', views.account_login, name="login"),
    path('logout/', views.account_logout, name="logout"),
]
```

 Now lets create those views. We will need forms for logging in and registering. The register form is provided by Django, we will create our registration form in a moment. We will also need html forms to display

###### account/views.py
``` python
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

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
```

Now create `account/forms.py` and add

###### account/forms.py
``` python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
```

And finally create the html files to display all this.

###### account/templates/account/login.html
``` html
{% extends "base.html" %}

{% block content %}

{% load crispy_forms_tags %}

<div class="container py-5">
    <h1>Login</h1>
    <form method="POST">
        {% csrf_token %}
        {{ login_form|crispy }}
        <button class="btn btn-primary" type="submit">Login</button>
    </form>
    <p class="text-center">Don't have an account? <a href="{% url 'register' %}">Create an account</a>.</p>
</div>

{% endblock %}
```

###### account/templates/account/register.html
``` html
{% extends "base.html" %}

{% block content %} 

{% load crispy_forms_tags %}         

<div class="container py-5">
	<h1>Register</h1>
	<form method="POST">
		{% csrf_token %}
		{{ register_form|crispy }}                    
		<button class="btn btn-primary" type="submit">Register</button>
	</form>
	<p class="text-center">If you already have an account, <a href="{% url 'login' %}">login</a> instead.</p>
</div>

{% endblock %}
```

And finally to easily access these pages lets add to the navbar some links

###### templates/navbar.html 
``` html
<nav class="navbar navbar-expand-md bg-light">
    <div class="container">
        <div class="collapse navbar-collapse" id="navbarToggle">
            <div class="navbar-nav pr-2">
                <a class="nav-item nav-link" href="{% url 'home' %}">Home</a>

                {% if user.is_authenticated %}
                <a class="nav-item nav-link" href="{% url 'logout' %}">Logout</a>
                {% else %}
                <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
                <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
                {% endif %}
            </div>
        </div>
    </div>
</nav>
```

Make migrations and run the server. Try creating a user, logging in, and logging out.
