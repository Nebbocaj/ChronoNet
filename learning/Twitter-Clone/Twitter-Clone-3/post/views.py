from django.shortcuts import render
from .models import Post
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F


def postListView(request):
    context = {}

    context["posts"] = Post.objects.personal_feed(request.user)

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
