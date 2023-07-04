
# Likes

First remove the console logs from the `view` function in the `Post` model.

There are a lot of ways to do this, lets create a new model for likes and dislikes together, call it `Vote`. Check out the documentation for this weird way of defining choices [https://docs.djangoproject.com/en/4.0/ref/models/fields/#choices].

``` python
class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerChoices(
        choices= [(LIKE, "Like"), (DISLIKE, "Dislike")]
        default=LIKE,
    )
    updated_on = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return str(self.post) + ":" + str(self.user) + ":" + str(self.vote)   
```

## First go

Now create a new view for making votes. For now it will return the users vote for that post, but later this would be done with an AJAX call so we don't redirect and can update the views left dynamically.

``` python
@login_required
def makeVote(request, post, vote):
    user = request.user
    post = Post.objects.get(id=post)

    voteState = vote

    oldVote = Vote.objects.filter(user=user, post=post).first() # we have to use first() since filter returns a set (fix later)
    if oldVote is not None: # user previously voted
        if vote == oldVote.vote: # undo a vote
            oldVote.delete()
            voteState = "none"
        else: # switch a vote
            oldVote.vote = vote
            oldVote.save()
    else: # user is making vote for the first time
        Vote.objects.create(post=post, user=user, vote=vote)

    return JsonResponse(voteState, safe=False)
```


Add a url path to this view, note the names in the url must match the names of the arguments of `make_vote`.

###### post/urls.py
``` python
from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.PostCreateView.as_view(), name='create_post'),   
    path('vote/<int:post>/<int:vote>', views.makeVote, name='make_vote'),
]
```

Now we add the buttons. First we want some fancy icons, so in `templates/base.html` add to the top the import

``` html  
    <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.11.2/css/all.css" 
        integrity="sha384-zrnmn8R8KkWl12rAZFt4yKjxplaDaT7/EUkKm7AovijfrQItFWR7O/JJn4DAa/gx" crossorigin="anonymous">
```

Then we will add the buttons in `post/templates/post/list_posts.html`. Note the second variable passed to the url must match the values of `LIKE` and `DISLIKE` in our Vote model, in this case the strings `'like'` and `'dislike'` respectively. 

``` html
            <p class="card-text text-muted h8">Remaining views: {{post.views_left}}</p>

            {% if user.is_authenticated %}
            <a href="#" onClick="document.getElementById('like_button').submit()"><i class="fas fa-thumbs-up"></i></a>   |   <a href="#" onClick="document.getElementById('dislike_button').submit()"><i class="fas fa-thumbs-down"></i></a>
            <form id="like_button" method="POST" action="{% url 'make_vote' post.id 'like' %}">
                {% csrf_token %}
                <input type="hidden">
            </form>
            <form id="dislike_button" method="POST" action="{% url 'make_vote' post.id 'dislike' %}">
                {% csrf_token %}
                <input type="hidden">
            </form>
            {% endif %}
        </div>
```

You can test everything is working, you will have to use the admin dashboard to track what views are doing what. Or you can just continue on, we will implement voting effects using AJAX.

## Second go

Hoo boy, we're changing everything.

We want to add a javascript section in `templates/base.html`, this will go just after importing the jquery and ajax libraries we also need. We put this at the end of the file

``` html  
    </main>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    {% block javascript %} {% endblock javascript %}

</body>
```

Now we are going to have a lot of files in which we haven't separated the logic, that is, we need to keep track of names and data in our heads to see where it is going.

To begin lets recode our view. Some notes: 
* We expect our request contains two arguments `post_id` and `vote`. 
* We now also return more information, namely the post ID we are working with, the views left for this post, and the users current vote status with `"none"` as the indicator that the user has no vote.

``` python
@login_required
def makeVote(request):
    if request.method =="POST" and request.is_ajax():
        # get values
        user = request.user
        post_id = int(request.POST.get("post_id",None))
        post = get_object_or_404(Post,pk=post_id)
        vote = request.POST.get("vote",None)

        voteState = vote # keeps track of updated vote (may have been switched or undone)
        oldVote = Vote.objects.filter(user=user, post=post).first() # we have to use first() since filter returns a set (fix later)
        if oldVote is not None: # user previously voted
            if vote == oldVote.vote: # undo a vote
                oldVote.delete()
                voteState = "none"
            else: # switch a vote
                oldVote.vote = vote
                oldVote.save()
        else: # user is making vote for the first time
            Vote.objects.create(post=post, user=user, vote=vote)
        
        return JsonResponse({
            "views_left":post.views_left,
            "vote_state":voteState,
            "post_id":post_id
            })
```

This requires us to change our urls, so now it looks like 

``` python
path('vote/', views.makeVote, name='make_vote'),
```

Now lets redo the buttons themselves, and it actually looks much nicer now. Some notes: 
* We give each button the class `vote_button` so we can attach an ajax call in a bit.
* We give each button the extra attribute `postID` so that ajax can extract which post was liked. 
* Each button has another attribute `vote` which must match the options in our Vote model. This is how ajax extracts what vote you made.

###### post/templates/post/list_posts.html
``` html
<div class="container">
    {% for post in posts %}
    <div class="card mb-4">
        <div class="card-body">
            <h2 class="card-title">{{ post.title }}</h2>
            <p class="card-text text-muted h6">{{ post.author }} | {{ post.created_on}} </p>
            <p class="card-text">{{post.content}}</p>
            <p class="card-text text-muted h8"> Remaining views: {{post.views_left}}</p>

            {% if user.is_authenticated %}
                <button class="vote_button btn" postID={{ post.id }} vote="like"><i class="fa fa-thumbs-up"></i></button>
                <button class="vote_button btn" postID={{ post.id }} vote="dislike"><i class="fa fa-thumbs-down"></i></button>
            {% endif %}
        </div>
    </div>
    {% endfor %}
</div>
```

And now we need the ajax itself. Create a new file `post/templates/post/like_button.js` and place the below code in it. Some notes:
* We use the previously noted attributes to extract information for the call.
* The names in our data must match what the view is expecting.
* We must use the CSRF token in our data.

###### post/templates/post/like_button.js
``` javascript
$(".vote_button").click(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // make POST ajax call
    postID = $(this).attr('postID')
    vote = $(this).attr('vote')
    $.ajax({
        type: 'POST',
        url: "{% url 'make_vote' %}",
        data: {'post_id': postID,'vote':vote,'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success: function (response) {
            console.log(response)
        },
        error: function (response) {
            alert(response["responseJSON"]["error"]);
        }
    })
})
```

And now we need to include this javascript in our code, and while it would be nice to place it in `list_posts.html`, that doesn't have access to the javascript content block (which apparently needs to be at the end of all html code). So we place it in `templates/home.html`, place it at the very end

``` html
{% block javascript %}
    <script>
    {% include 'post/like_button.js' %}
    </script>
{% endblock javascript %}
```

And check everything is working by liking some posts and seeing if the right vote state is printed in the console along with all the other data.

## Views left

Lets have the views left update. Add that logic into our view, its not too bad, just takes up space.

``` python
@login_required
def makeVote(request):
    if request.method =="POST" and request.is_ajax():
        # get values
        user = request.user
        post_id = int(request.POST.get("post_id",None))
        post = get_object_or_404(Post,pk=post_id)
        vote = request.POST.get("vote",None)

        # update users vote and views left of post
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
```

Now check that when we like something, the object printed in the console has a different views_left.

Now we can have the ajax update the views left html. This first requires us to wrap the views left in an html `<span>` so ajax can find it, but each post needs a unique ID, so then the html is instead

``` html
<p class="card-text text-muted h8"> Remaining views: <span id="views_left_post{{post.id}}">{{post.views_left}}</span></p>
```

And now in the ajax we can find that element and update it, so the ajax success function is now

``` javascript
success: function (response) {
    selector = document.getElementById("views_left_post" + postID)
    $(selector).text(response.views_left)
},
```

And now check everything is working.

## Show vote

Finally lets have the like buttons display their state. First we need to identify the liked posts, so in the view `postListView` our code now looks like (there really must be a better way)

``` python
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
```

Then in the html `list_posts.html` we want to have the buttons `active` if selected, so now the buttons look like

``` html
            {% if user.is_authenticated %}
                {% if post in liked_posts %}
                    <a href="#" class="vote_button btn btn-primary active" postID={{ post.id }} vote="like"><i class="fa fa-thumbs-up"></i></a>
                {% else %}
                    <a href="#" class="vote_button btn btn-primary" postID={{ post.id }} vote="like"><i class="fa fa-thumbs-up"></i></a>
                {% endif %}
                {% if post in disliked_posts %}
                    <a href="#" class="vote_button btn btn-primary active" postID={{ post.id }} vote="dislike"><i class="fa fa-thumbs-down"></i></a>
                {% else %}
                    <a href="#" class="vote_button btn btn-primary" postID={{ post.id }} vote="dislike"><i class="fa fa-thumbs-down"></i></a>
                {% endif %}
            {% endif %}
```

Then in our ajax we want to update the buttons, so now our success function looks like

``` javascript
        success: function (response) {
            selector = document.getElementById("views_left_post" + postID)
            $(selector).text(response.views_left)

            like_button = $('[vote="like"][postID=' + postID + ']');
            dislike_button = $('[vote="dislike"][postID=' + postID + ']');
            like_button.removeClass("active")
            dislike_button.removeClass("active")
            if (response.vote_state == "like") {
                like_button.addClass("active")
            } else if (response.vote_state == "dislike") {
                dislike_button.addClass("active")
            }
        },
```

Now check the buttons change when you click on them.