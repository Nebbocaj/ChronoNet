# https://blog.logrocket.com/use-django-rest-framework-to-build-a-blog/
import requests

baseURL = "http://127.0.0.1:8000/api/"

class Author(object):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __str__(self):
        return "({}) {}".format(self.id, self.username)

class Post(object):
    def __init__(self, author, title, content, id):
        self.author = Author(**author)
        self.title = title
        self.content = content
        self.id = id

    def __str__(self):
        return "({}) Title: {}\n\tAuthor: {}\n\tContent: {}".format(
            self.id, self.title, self.author, self.content)


def getPosts(auth=None):
    params = {'format': 'json'}
    response = requests.get(
        url=baseURL + "posts/",
        params=params,
        auth=auth
    )
    return list(map(lambda x: Post(**x), response.json()))


def getPost(postID, auth=None):
    params = {'format': 'json'}
    response = requests.get(
        url=baseURL + "posts/{}/".format(postID),
        params=params,
        auth=auth
    )
    return Post(**response.json())


def createPost(title, content, auth):
    post_data = {'title': title, 'content': content}
    response = requests.post(
        url=baseURL + "posts/create/",
        data=post_data,
        auth=auth
    )
    return Post(**response.json())


def getFeed(auth):
    params = {'format': 'json'}
    response = requests.get(
        url=baseURL + "posts/feed/",
        params=params,
        auth=auth
    )
    return list(map(lambda x: Post(**x), response.json()))


def vote(postID, vote, auth):
    post_data = {'vote': vote}
    response = requests.post(
        url=baseURL + "posts/{}/vote/".format(postID),
        data=post_data,
        auth=auth
    )
    return response.json()


def follow(toUserID, auth):
    response = requests.post(
        url=baseURL + "users/{}/follow/".format(toUserID),
        auth=auth
    )
    return response.json()


def createAccount(username, password):
    post_data = {'username': username, 'password': password}
    response = requests.post(
        url=baseURL + "users/create/", 
        data=post_data
    )
    return response.json()


def getUser(userID):
    params = {'format': 'json'}
    response = requests.get(
        url=baseURL + "users/{}/".format(userID), 
        params=params
    )
    return response.json()
