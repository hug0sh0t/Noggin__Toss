from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL 


# class FollowerRelation(models.Model):
#      user = models.ForeignKey(User, on_delete=models.CASCADE, default="", editable=False)
#      profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
#      timestamp = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', default='/parking/test.png', null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    createBadge = models.IntegerField(default = 0,blank=True)
    impactBadge = models.IntegerField(default = 0,blank=True)
    hermesBadge = models.IntegerField(default = 0,blank=True)
    FavoredBadge = models.IntegerField(default = 0,blank=True)
    
    
def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)
