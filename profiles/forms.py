from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from noggins.models import Noggin
import django_filters
from crispy_forms.helper import FormHelper
from django.core.files.base import ContentFile
from django_filters import CharFilter
User = get_user_model()

#affects user update form

class UserProfileForm(forms.ModelForm):
    location = forms.CharField(required=False)
    bio = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['user__username','followers']


    def get_followers(self, obj):
        return obj.user.followers

class NogginFilter(django_filters.FilterSet):
    class Meta:
        model = Noggin
        fields = ['content']

    def get_content(self, obj):
        return obj.content



class UserFilter(django_filters.FilterSet):
    username = CharFilter(label="")
    class Meta:
        model = User
        fields = ['username']

    def get_username(self, obj):
        return obj.user.username



class ProfileForm(forms.ModelForm):
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ['last_name','first_name','location', 'avatar', 'bio','email']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in ProfileForm.Meta.fields:
            self.fields[field].label = False


class ProfileBasicForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email_address = forms.CharField(required=False)
    location = forms.CharField(required=False)
    bio = forms.CharField(required=False)




