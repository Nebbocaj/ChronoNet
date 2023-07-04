
import random
import apiCalls as api
from requests.auth import HTTPBasicAuth

class Bot(object):
    def __init__(self, username):
        self.username = username
        self.password = "pass"
        
        self.auth = HTTPBasicAuth(self.username, self.password)

        self.postContents = []
    
    def createAccount(self):
        return api.createAccount(self.username, self.password)

    def makePost(self, content_generator):
        
        # CONTENT
        num_posts_considered = 5
        seperator = "\n#####\n"

        prompt = ""
        if len(self.postContents) > 0:
            prompt = seperator + seperator.join(self.postContents[-num_posts_considered:]) + seperator
            print("\n--- prompt:\n", prompt)
        
        generated_text = content_generator.generate(
            prompt=prompt, 
            return_as_list=True, 
            max_length= len(prompt.split(" ")) + 100 # want length of prompt plus 100, so the new post has max 100 words
            )[0]
        
        if len(prompt) > 0:
            generated_text = generated_text[len(prompt)-1:] # remove prompt

        print("\n--- generated :\n", generated_text)

        generated_text = generated_text.split(seperator)[0] # remove extra posts made

        generated_text = generated_text[:499] # django wont accept posts longer then 500 chars

        if generated_text[-1] != '.':
            generated_text = generated_text.rsplit('.', 1)[0] + '.' # remove unfinished last sentence
        
        print("\n--- cleaned:\n", generated_text)

        self.postContents.append(generated_text)

        # TITLE
        generated_title = "title"
        
        return api.createPost(generated_title, generated_text, self.auth)
    
    def browse(self):
        if random.random() < 0.5:
            return self.interactWithPosts(api.getFeed(self.auth))
        else:
            return self.interactWithPosts(api.getPosts(self.auth))

        
    def interactWithPosts(self, posts):
        likedPosts = []
        followedUsers = []

        for post in posts:
            if random.random() < 0.1:
                api.vote(post.id, "like", self.auth)
                likedPosts.append(post.id)
            
            if random.random() < 0.1:
                api.follow(post.author.id, self.auth)
                followedUsers.append(post.author.id)
        
        return likedPosts, followedUsers
    