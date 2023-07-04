import json
from typing import Dict
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Post, Vote
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def postListView(request):
    context = {}

    context["posts"] = Post.objects.personal_feed(request.user)
    
    context["liked_posts"] = []
    context["disliked_posts"] = []
    if request.user.is_authenticated:
        for post in context["posts"]:
            vote = Vote.objects.filter(post=post, user=request.user).first()
            if vote is not None:
                if vote.vote == Vote.LIKE:
                    context["liked_posts"].append(post)
                elif vote.vote == Vote.DISLIKE:
                    context["disliked_posts"].append(post)

    return render(request, "home.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        # on validate we set the author, other fields are either auto or set by the user
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def makeVote(request):
    if request.method =="POST" and request.is_ajax():
        # get values
        user = request.user
        post_id = int(request.POST.get("post_id",None))
        post = get_object_or_404(Post,pk=post_id)
        vote = request.POST.get("vote",None)

        # update users vote and view count of post
        like_reward = 5
        dislike_reward = -1

        voteState = vote # keeps track of updated vote (may have been switched or undone)
        oldVote = Vote.objects.filter(user=user, post=post).first() # we have to use first() since filter returns a set (fix later)
        if oldVote is not None: # user previously voted
            if vote == oldVote.vote: # undo a vote
                oldVote.delete()
                voteState = "none"
                if vote == Vote.LIKE:
                    post.views_left -= like_reward
                else:
                    post.views_left -= dislike_reward
            else: # switch a vote
                oldVote.vote = vote
                oldVote.save()
                if vote == Vote.LIKE:
                    post.views_left += like_reward - dislike_reward
                else:
                    post.views_left += dislike_reward - like_reward
        else: # user is making vote for the first time
            Vote.objects.create(post=post, user=user, vote=vote)
            if vote == Vote.LIKE:
                post.views_left += like_reward
            else:
                post.views_left += dislike_reward

        post.save() # we altered the view count
        
        return JsonResponse({
            "views_left":post.views_left,
            "vote_state":voteState,
            "post_id":post_id
            })


