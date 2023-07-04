
# View count

Lets update the view count in the most basic way possible, every time a post is queried through `postListView` we decrement the view count. In `postListView` add the database update query using a fancy F function given by Django (see the link in code for more).

``` python
def postListView(request):
    context = {}

    # later this will be unique to each person
    posts = Post.objects.filter(views_left__gte=1).order_by('-created_on')

    # decrement view count by one, need something more sophisticated later
    posts.update(views_left=F('views_left')-1) # https://docs.djangoproject.com/en/4.0/ref/models/expressions/#f-expressions

    context["posts"] = posts

    return render(request, "home.html", context)
```

Run the server and check every time you refresh the page the counter decreases. 

We probably want the counter to decrement only when a user sees a post for the first time, this means don't count when the user isn't logged in or they have seen the post before.

This could be done in lots of different ways, I'll be letting the Post model keep track of everyone who has seen it. The view function attached to our post will handle most of the logic of tracking view counts (I don't like manually updating the views_left attribute, is there a better way?). Then our custom manager will just get all posts that still have views and order them, followed by making sure they each get viewed.

``` python
from django.db import models
from django.contrib.auth.models import User


class PostManager(models.Manager):
    def personal_feed(self, user):

        # later this can be unique to each person
        posts = self.filter(views_left__gte=1).order_by('-created_on')

        if user.is_authenticated:
            [post.view(user) for post in posts]
                
        return posts


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")

    views_allowed = models.IntegerField(default=100)
    views_left = models.IntegerField(default=100)
    views = models.ManyToManyField(User, blank=True, related_name="views")

    objects = PostManager()

    def view(self, user):
        print("post " + self.title + " was viewed by " + user.username)

        if user and user not in self.views.all():
            print("for the first time")
            self.views.add(user)
            self.views_left = self.views_allowed - self.views.count()
            self.save()

    def __str__(self):
        return self.title
```

We can use our manager to clean up the postListView view, which is now

``` python
def postListView(request):
    context = {}

    context["posts"] = Post.objects.personal_feed(request.user)

    return render(request, "home.html", context)
```
Make migrations to update the database.
Run the server and create a new user to login with. Check the console log to see if new views are triggered, and refresh to see if the view is triggered again, but without it being new.