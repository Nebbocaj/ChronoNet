from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

#The actual profile class where everything is stored
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=12, blank = True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    following = models.ManyToManyField("self", blank=True, symmetrical=False)
    
    def __str__(self):
        return self.user.username + ":" + self.nickname
    
    def follow(self, viewingProfile):
        following = True

        if viewingProfile in self.following.all():
            following = False
            self.following.remove(viewingProfile)
        else:
            self.following.add(viewingProfile)
        
        self.save()

        return following

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, nickname=instance.username)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()