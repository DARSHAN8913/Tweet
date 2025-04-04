from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser to include additional profile information
    """
    bio = models.TextField(max_length=160, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    website = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    # followers = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    
    def __str__(self):
        return self.username
    
    @property
    def follower_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()