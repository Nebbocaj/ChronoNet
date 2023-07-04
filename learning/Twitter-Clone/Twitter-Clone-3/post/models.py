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
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")

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
