import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Exists, OuterRef
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from django.core.paginator import Paginator
import random


class PostManager(models.Manager):
    def get_queryset(self):
        result = super().get_queryset().order_by('-created_on')
        result = result.filter(expires_on__gt=timezone.now())
        return result # for testing it helps to have posts to work with

    def personal_feed(self, user):

        extraSet = []
        # currently just selects posts from who we follow
        following_posts = self.filter(author__profile__in=user.profile.following.all())
        for u in user.profile.following.all():
            extra_posts = self.filter(author__profile__in=u.user.profile.following.all())
            for p in extra_posts:
                if random.randint(1,100) < 25:
                    extraSet.append(p)
        for e in extraSet:
            following_posts |= self.filter(title=e.title, content = e.content, author = e.author)
        return following_posts
    
    def explore_feed(self):

        posts = self.all()

        return posts
    
    def paginate(self, posts, page_number=None):
        paginator = Paginator(posts, 5)
        page_obj = paginator.get_page(page_number)
        return page_obj
    
    def annotateWithVote(self, posts, user):
        liked = Vote.objects.filter(post=OuterRef('pk'), user=user, vote=Vote.LIKE)
        disliked = Vote.objects.filter(post=OuterRef('pk'), user=user, vote=Vote.DISLIKE)
        return posts.annotate(liked=Exists(liked), disliked =Exists(disliked))

        

def create_expiration():
    return timezone.now() + datetime.timedelta(hours=1)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = MarkdownField(rendered_field='text_rendered', validator=VALIDATOR_STANDARD, use_admin_editor=False)
    text_rendered = RenderedMarkdownField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")

    created_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField(default= create_expiration)

    objects = PostManager()
    
    def vote(self, user, vote):

        maxReward = 30
        minReward = 1
        time_decay = 5

        time_alive = timezone.now() - self.created_on
        days = time_alive / datetime.timedelta(days=1)

        reward = minReward + (maxReward - minReward) / (1.0 + (days ** 2) / time_decay)

        # we have to use first() since filter returns a set (fix later)
        oldVote = Vote.objects.filter(user=user, post=self).first()
        if oldVote is not None:  # user previously voted
            if vote == oldVote.vote:  # undo a vote
                oldVote.delete()
                if vote == Vote.LIKE:
                    # UNDO A LIKE
                    # ---------------------------
                    self.expires_on -= datetime.timedelta(minutes=reward)
                    # ----------------------------
                else:
                    # UNDO A DISLIKE
                    # ---------------------------
                    self.expires_on += datetime.timedelta(minutes=reward)
                    # ---------------------------
            else:  # switch a vote
                oldVote.vote = vote
                oldVote.save()
                if vote == Vote.LIKE:
                    # SWITCH FROM DISLIKE TO LIKE
                    # ---------------------------
                    self.expires_on += datetime.timedelta(minutes=2*reward)
                    # ---------------------------
                else:
                    # SWITCH FROM LIKE TO DISLIKE
                    # ---------------------------
                    self.expires_on -= datetime.timedelta(minutes=2*reward)
                    # ---------------------------
        else:  # user is making vote for the first time
            Vote.objects.create(post=self, user=user, vote=vote)
            if vote == Vote.LIKE:
                # ADD A LIKE
                # ---------------------------
                self.expires_on += datetime.timedelta(minutes=reward)
                # ---------------------------
            else:
                # ADD A DISLIKE
                # ---------------------------
                self.expires_on -= datetime.timedelta(minutes=reward)
                # ---------------------------
        
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