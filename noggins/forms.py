from django.conf import settings
from django import forms
from .models import Noggin, Comment
from django.shortcuts import redirect
from crispy_forms.helper import FormHelper
NOGGIN_FULL = settings.NOGGIN_FULL

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        for field in CommentForm.Meta.fields:
            self.fields[field].label = False

class NogginForm(forms.ModelForm):
    class Meta:
        model = Noggin
        fields = ['content', 'image', 'video']
    # fields should also contain content  
    # noggin creation is handled inside of REST api, manipulated in React 
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > NOGGIN_FULL:
            raise forms.ValidationError("This Noggin is Way Too long")
        return content

    

