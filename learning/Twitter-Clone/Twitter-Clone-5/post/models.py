from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import Choices


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
        if user and user not in self.views.all():
            self.views.add(user)
            self.views_left = self.views_allowed - self.views.count()
            self.save()

    def __str__(self):
        return self.title


class Vote(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(
        max_length=100,
        choices= [(LIKE, "Like"), (DISLIKE, "Dislike")],
        default=LIKE,
    )
    updated_on = models.DateTimeField(auto_now_add=True)        

    def __str__(self):
        return str(self.post) + ":" + str(self.user) + ":" + str(self.vote)