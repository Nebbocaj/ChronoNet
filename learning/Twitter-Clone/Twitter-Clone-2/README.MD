
# Setup

Create the app `post` and add it to the settings.

# Post

## Seeing posts

Lets start with a simple post model.

###### post/models.py
``` python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    views_left = models.IntegerField(default=100)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
```

Now for the views. Filtering is weird, in order to only display posts with time left to live have to use underscores, weird. https://docs.djangoproject.com/en/4.0/ref/models/querysets/

###### post/views.py
``` python
from django.shortcuts import render
from .models import Post

def postListView(request):
    context ={}

    # later this will be unique to each person
    context["posts"] = Post.objects.filter(views_left__gte=1).order_by('-created_on')
         
    return render(request, "home.html", context)
```

And lets add the url to view the latest posts. We will actually just view posts in home, so rewrite the base url to route to the above view.
``` python
import post.views as post_views
 ...
    path('', post_views.postListView, name='home'),    
```

And lets view those posts in home, but lets do it in a new html document we can insert later. I'll call it `list_posts.html`.

###### account/templates/account/list_posts.html
``` html
<div class="container">
    {% for post in posts %}
    <div class="card mb-4">
        <div class="card-body">
            <h2 class="card-title">{{ post.title }}</h2>
            <p class="card-text text-muted h6">{{ post.author }} | {{ post.created_on}} </p>
            <p class="card-text">{{post.content}}</p>
            <p class="card-text text-muted h8">Remaining views: {{post.views_left}}</p>
        </div>
    </div>
    {% endfor %}
</div>
```

and add this in the home html. I just replaced what was there, so now

###### templates/home.html
``` html
{% extends 'base.html' %}
{% block title %}Home{% endblock %}
{% block content %}

{% if posts %}
{% include 'list_posts.html' %}
{% else %}

Welcome to our webpage!

{% endif %}

{% endblock %}
```

Now migrate changes, run server, and see if everything is working.

If later you want to have a detailed post view, check the resource at the bottom for building a blog in which they create a detailed view of a post.

I created some posts with admin so I could make sure things looked ok, but not necessary since we will create posting functionality right now. 

## Making posts

Lets start with a url to make a post. Create `post/urls.py` and add

###### post/urls.py
``` python
from . import views

urlpatterns = [
    path('new/', views.PostCreateView.as_view(), name='create_post'),    
]
```

Then make sure to add these urls in our base url file
##### config/urls.py
``` python
    path('post/', include('post.urls')),
```

Then the view, make sure only people logged in can make a post. I don't totally get them, but it seems to make everything easier, so I'll use a class based view that automatically creates objects to our database.

###### post/views.py
``` python
...
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

...

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        # on validate we set the author, other fields are either auto or set by the user
        form.instance.author = self.request.user
        return super().form_valid(form)
```

Now we need the html file to show this view.
###### post/templates/post/post_new.html
``` html
{% extends "base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<div class="container">
    <form method="POST">
        {% csrf_token %}
        <fieldset class="form-group">
            {{ form | crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-primary" type="submit">Post</button>
        </div>
    </form>
</div>
{% endblock content %}
```

And now we just need a button to get us to that view. Lets add that to the home page.

###### templates/home.html
``` html
...

<div class="container mb-4 text-center">
{% if user.is_authenticated %}
<a class="btn btn-primary" href="{% url 'create_post' %}">Create post</a>
{% endif %}
</div>

...
```

Now login and try to make a post.

# Resources
- https://djangocentral.com/building-a-blog-application-with-django/