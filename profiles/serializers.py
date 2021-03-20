from rest_framework import serializers
from .models import Profile
import django_filters
import base64, uuid
from crispy_forms.helper import FormHelper
#creates images for user from user

# search filter enginer


class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.ImageField(max_length=None,use_url=True, required=False)
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "avatar",
            "id",
            "bio",
            "location",
            "followers",
            "follower_count",
            "following_count",
            "is_following",
            "username",
        ]

    def get_is_following(self, obj):
        is_following = False
        context = self.context
        request = context.get("request")
        if request: 
            user = request.user
            is_following = user in obj.followers.all()
        return is_following
    
    def get_followers(self, obj):
        context = self.context
        request = context.get("request")
        if request: 
            qs = Profile.objects.filter(user=obj.user)
            user_qs = qs.first()
            return user_qs.user_id

    def get_name(self, obj):
        return obj.user.username 
    
    def get_avatar(self, obj):
        return obj.user.avatar

    def get_first_name(self, obj):
        return obj.user.first_name
        
    def get_last_name(self, obj):
        return obj.user.last_name    

    def get_username(self, obj):
        return obj.user.username    
  
    def get_following_count(self, obj):
        return obj.user.following.count()
    
    def get_follower_count(self, obj):
        return obj.followers.count()
 
