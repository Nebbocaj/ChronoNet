# https://blog.logrocket.com/use-django-rest-framework-to-build-a-blog/

from django.shortcuts import get_object_or_404
from rest_framework import generics, exceptions, permissions, views
from api import serializers
from django.contrib.auth.models import User
from post.models import Post, Vote
from rest_framework.response import Response

#Each individual post
class PostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

#The page to create a post
class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # we know the author since they must be logged in
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#The post explore page
class PostExplore(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    
    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            return Post.objects.explore_feed(self.request.user)
        else:
            return Post.objects.explore_feed() 

#User post feed
class PostFeed(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.personal_feed(self.request.user)

#Ability to vote on a post via the API
class PostVote(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = serializers.VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        postID = kwargs.get('pk', None)
        vote = self.request.POST.get("vote", None)

        if vote:
            post = get_object_or_404(Post, pk=postID)
            user = request.user

            post.vote(user, vote)

            newVote = Vote.objects.filter(post=post, user=user).first()
            if newVote:
                # found out what to do here by looking at what the retrieve mixin does
                serializer = self.get_serializer(newVote) 
                return Response(serializer.data)
            else:
                # no vote, need to craft a response
                return Response({"detail":"there is no vote by this user for this post"})
        else:
            exceptions.ParseError(detail="vote parameter must be set (.../vote/?vote=like)")

#Creat a new user
class UserCreate(generics.CreateAPIView):
    model = User
    serializer_class = serializers.UserSerializer

#Get the user view
class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

#Follow a different user
class UserFollow(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        userID = kwargs.get('pk', None)

        userFrom = request.user
        userTo = get_object_or_404(User, pk=userID)

        following = userFrom.profile.follow(userTo.profile)
        return Response(following)