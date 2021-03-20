import random
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.humanize.templatetags import humanize
from profiles.models import Profile
from django.db.models import Count
User = settings.AUTH_USER_MODEL

class NogginLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    noggin = models.ForeignKey("Noggin", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class NogginEyeball(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    noggin = models.ForeignKey("Noggin", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return 'Viewer:  {} Time Seen: {} '.format(self.user, self.timestamp)

class Comment(models.Model):
    post = models.ForeignKey("Noggin",on_delete=models.CASCADE,related_name='comments',null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    commentlike = models.ManyToManyField(User, related_name='commenter', blank=True)
    body = models.TextField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']
   
    # Queryset Return
    def __str__(self):
        return 'ID> {} likes>  {} USER {},  VALID_YES_NO: {}'.format(self.id,
                self.commentlike.count(), self.user, self.active)

class NogginQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True) # [x.user.id for x in profiles]
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-timestamp")   
        
class NogginManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return NogginQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

class Noggin(models.Model):
    # map to SQl 
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noggins", null=True)
    likes = models.ManyToManyField(User, related_name='noggin_user', blank=True, through=NogginLike)
    eyeball_count = models.ManyToManyField(User, related_name='noggin_view', blank=True,
            through=NogginEyeball)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, null=True)
    video = models.FileField(upload_to='videos/%Y/%m/%d/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = NogginManager()

    class Meta:
        ordering = ["-timestamp"]
 
    @property
    def is_relay(self):
        return self.parent != None


