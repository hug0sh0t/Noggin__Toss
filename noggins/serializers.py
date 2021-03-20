from django.conf import settings
from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import Noggin, Comment
import base64, uuid
from django.core.files.base import ContentFile

NOGGIN_FULL = settings.NOGGIN_FULL
NOGGIN_ACTION_OPTIONS = settings.NOGGIN_ACTION_OPTIONS

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,') # format ~= data:image/X,
            ext = format.split('/')[-1] # guess file extension
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)

class Base64Field(serializers.FileField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64Field, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "mp4" if extension == "mp4" else extension

        return extension


class NogginActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    video = serializers.FileField(max_length=None, use_url=True, required=False)
    
    def validate_action(self, value):
        value = value.lower().strip()
        if not value in NOGGIN_ACTION_OPTIONS:
            raise serializers.ValidationError("INVALID NOGGIN ACTION")
        return value

class NogginCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True) # serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    video = Base64Field(max_length=None, use_url=True, required=False)
    timestamp = serializers.DateTimeField(format="%m-%d-%Y%H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Noggin
        fields = ['user','id','content','image','video','likes', 'timestamp']
 
    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > NOGGIN_FULL:
            raise serializers.ValidationError("this Noggin is too Long")
        return value

    # def get_user(self, obj):
    #    return obj.user.id


class NogginSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(source='noggin.Comment',read_only=True)
    eyeballs = serializers.SerializerMethodField(source='noggin.NogginEyeball',read_only=True)
    parent = NogginCreateSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    video = serializers.FileField(max_length=None, use_url=True, required=False)
    timestamp = serializers.DateTimeField(format="%m-%d-%Y %H:%M", required=False, read_only=True)
    class Meta:
        model = Noggin
        fields = ['comments','eyeballs','user','id','content','likes', 'image','video','parent','timestamp']
    
    def get_eyeballs(self, obj):
        return obj.eyeball_count.count()
     
    def get_comments(self, obj):
        return obj.comments.count()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_content(self, obj):
        return obj.parent.content

    def get_image(self, obj):
        return obj.parent.image

    def get_video(self, obj):
        return obj.parent.video

    # def get_user(self, obj):
    # return obj.user.id
    
