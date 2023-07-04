import datetime
import json
from typing import Dict
from django.http import Http404, HttpResponseNotFound
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Post, Vote
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

#The individual user feed for each user
def postListViewUserFeed(request):
    context = {}

    posts = Post.objects.personal_feed(request.user)
    posts = Post.objects.annotateWithVote(posts, request.user)
    posts = Post.objects.paginate(posts, request.GET.get('page'))

    context["page_obj"] = posts

    return render(request, "home.html", context)

#The general explore page with every post that has been created
def postListViewExplore(request):
    context = {}

    posts = Post.objects.explore_feed()
    if request.user.is_authenticated:
        posts = Post.objects.annotateWithVote(posts, request.user)
    posts = Post.objects.paginate(posts, request.GET.get('page'))

    context["page_obj"] = posts

    return render(request, "home.html", context)

#The view where a user can create a post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        # on validate we set the author, other fields are either auto or set by the user
        form.instance.author = self.request.user
        return super().form_valid(form)

#Method to like or dislike a post
@login_required
def makeVote(request):
    if request.method == "POST" and request.is_ajax():
        # get values
        user = request.user
        post_id = int(request.POST.get("post_id", None))
        try:
            post = get_object_or_404(Post, pk=post_id)
        except Http404:
            return JsonResponse({
                "expires": 0,
                "vote_state": "none",
                "post_id": post_id
            })
        vote = request.POST.get("vote", None)

        post.vote(user, vote)
        
        voteState = vote
        if Vote.objects.filter(user=user, post=post).first() is None:
            voteState = "none"

        return JsonResponse({
            "expires": post.expires_on,
            "vote_state": voteState,
            "post_id": post_id
        })

#The functionality to delete an individual post that was created by the logged in user
@login_required
def deletePost(request):
    if request.method == "POST" and request.is_ajax():
        # get values
        user = request.user
        post_id = int(request.POST.get("post_id", None))
        try:
            post = get_object_or_404(Post, pk=post_id)
        except Http404:
            return JsonResponse({"deleted": True})
        

        if post.author == user: # make sure the logged in user is only deleting their own post
            post.delete()


        return JsonResponse({"deleted": True})

#Get the updated time on a post
def getPostsTime(request):
    if request.method == "POST" and request.is_ajax():

        post_ids = request.POST.getlist('post_ids[]')

        result = []
        for post_id in post_ids:
            try:
                expires = get_object_or_404(Post, pk=post_id).expires_on
            except Http404:
                expires = 0

            result.append(expires)

        return JsonResponse({
            "postIDs": post_ids,
            "expirations": result,
        })
